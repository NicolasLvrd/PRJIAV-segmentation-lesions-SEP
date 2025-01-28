import SimpleITK as sitk
import numpy as np
import cv2
import os
import torch
from torch.utils.data import Dataset


def load_nii_file(file_path):
    """
    Load a NIfTI file using SimpleITK and return a NumPy array.
    """
    image = sitk.ReadImage(file_path)
    data = sitk.GetArrayFromImage(image)  # Converts to a NumPy array (z, y, x)
    return data


def preprocess_slice(slice_data, target_size=(256, 256)):
    """
    Normalize and resize a 2D slice from the 3D image.
    """
    slice_data = (slice_data - np.min(slice_data)) / (np.max(slice_data) - np.min(slice_data))  # Normalize to [0, 1]
    resized_slice = cv2.resize(slice_data, target_size)
    return resized_slice


class BrainDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        """
        Args:
            root_dir (str): Directory with all the .nii.gz files.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        self.root_dir = root_dir
        self.transform = transform

        # List all flair and consensus files
        self.flair_files = sorted(
            [f for f in os.listdir(root_dir) if f.endswith('_flair_0.nii.gz')]
        )
        self.consensus_files = sorted(
            [f for f in os.listdir(root_dir) if f.endswith('_consensus.nii.gz')]
        )

        assert len(self.flair_files) == len(self.consensus_files), "Mismatch between flair and consensus files"

    def __len__(self):
        return len(self.flair_files)

    def __getitem__(self, idx):
        # Load flair and consensus files
        flair_path = os.path.join(self.root_dir, self.flair_files[idx])
        consensus_path = os.path.join(self.root_dir, self.consensus_files[idx])

        # Load the NIfTI images
        flair_image = sitk.GetArrayFromImage(sitk.ReadImage(flair_path))
        consensus_mask = sitk.GetArrayFromImage(sitk.ReadImage(consensus_path))

        # Select the middle slice along the depth dimension
        middle_slice = flair_image.shape[0] // 2
        flair_image = flair_image[middle_slice, :, :]  # Select slice [H, W]
        consensus_mask = consensus_mask[middle_slice, :, :]  # Select slice [H, W]

        # Convert to torch tensors
        flair_image = torch.tensor(flair_image, dtype=torch.float32).unsqueeze(0)  # Add channel dimension [C, H, W]
        flair_image = flair_image / flair_image.max()  # Normalize to [0, 1]
        consensus_mask = torch.tensor(consensus_mask, dtype=torch.int64)  # Masks are integers

        # Prepare target in Mask R-CNN format
        target = {}
        target['boxes'], target['labels'], target['masks'] = self._process_mask(consensus_mask)
        target['image_id'] = torch.tensor([idx])

        if self.transform:
            flair_image, target = self.transform(flair_image, target)

        return flair_image, target

    def _process_mask(self, mask):
        """
        Process the consensus mask to extract bounding boxes, labels, and binary masks.

        Args:
            mask (Tensor): Segmentation mask of shape (H, W, D).

        Returns:
            boxes (Tensor): Bounding boxes [xmin, ymin, xmax, ymax] for each object.
            labels (Tensor): Labels for each object (default: 1 for single-class segmentation).
            masks (Tensor): Binary masks for each object.
        """
        masks = mask > 0  # Assume nonzero values are the mask regions
        masks = masks.type(torch.uint8)  # Ensure masks are binary

        # Get object IDs, excluding background (0)
        obj_ids = torch.unique(mask)
        obj_ids = obj_ids[obj_ids != 0]

        # Handle empty masks (no objects)
        if len(obj_ids) == 0:
            return (
                torch.zeros((0, 4), dtype=torch.float32),  # No boxes
                torch.zeros((0,), dtype=torch.int64),  # No labels
                torch.zeros((0, *mask.shape), dtype=torch.uint8),  # No masks
            )

        boxes = []
        binary_masks = []
        for obj_id in obj_ids:
            obj_mask = (mask == obj_id).type(torch.uint8)
            pos = torch.where(obj_mask > 0)

            # Skip objects with no valid positions
            if len(pos[0]) == 0:
                continue

            xmin = torch.min(pos[1])
            xmax = torch.max(pos[1])
            ymin = torch.min(pos[0])
            ymax = torch.max(pos[0])

            boxes.append([xmin.item(), ymin.item(), xmax.item(), ymax.item()])
            binary_masks.append(obj_mask)

        # Convert to tensors
        boxes = torch.tensor(boxes, dtype=torch.float32)
        binary_masks = torch.stack(binary_masks, dim=0)

        return boxes, torch.ones(len(boxes), dtype=torch.int64), binary_masks
