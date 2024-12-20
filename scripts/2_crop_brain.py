import SimpleITK as sitk
import argparse
import numpy as np
import os

def compute_minimal_bounding_box(image_files: list[str]) -> tuple[tuple[int], tuple[int]]:
    """
    Compute the minimal bounding box that encompasses the non-zero regions across all given images.
    """
    min_bounds = np.array([np.iinfo(np.int32).max] * 3, dtype=int)
    max_bounds = np.array([np.iinfo(np.int32).min] * 3, dtype=int)

    for file in image_files:
        image = sitk.ReadImage(file)
        array = sitk.GetArrayFromImage(image)

        # Get non-zero indices
        non_zero_indices = np.argwhere(array > 0)

        # Update bounds
        if non_zero_indices.size > 0:  # Ensure there are non-zero values
            min_bounds = np.minimum(min_bounds, non_zero_indices.min(axis=0))
            max_bounds = np.maximum(max_bounds, non_zero_indices.max(axis=0))

    return tuple(min_bounds), tuple(max_bounds + 1)  # +1 for inclusive upper bounds


def crop_and_save_images(image_files, min_bounds, max_bounds, output_dir):
    """
    Crop all images based on the computed bounding box and save them.
    """
    os.makedirs(output_dir, exist_ok=True)
    for file in image_files:
        image = sitk.ReadImage(file)
        array = sitk.GetArrayFromImage(image)

        # Crop using the bounds
        cropped_array = array[min_bounds[0]:max_bounds[0],
                        min_bounds[1]:max_bounds[1],
                        min_bounds[2]:max_bounds[2]]

        # Convert back to SimpleITK image
        cropped_image = sitk.GetImageFromArray(cropped_array)

        # Update metadata
        origin = image.GetOrigin()
        spacing = image.GetSpacing()
        direction = image.GetDirection()

        new_origin = (
            origin[0] + spacing[0] * min_bounds[2],  # Adjust x-origin
            origin[1] + spacing[1] * min_bounds[1],  # Adjust y-origin
            origin[2] + spacing[2] * min_bounds[0],  # Adjust z-origin
        )

        cropped_image.SetOrigin(new_origin)
        cropped_image.SetSpacing(spacing)
        cropped_image.SetDirection(direction)

        # Save cropped image
        output_file = os.path.join(output_dir, os.path.basename(file))
        sitk.WriteImage(cropped_image, output_file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help='Input directory', required=True)
    parser.add_argument('--output', type=str, help='Output directory', required=True)
    args = parser.parse_args()

    image_files = [os.path.join(args.input, f) for f in os.listdir(args.input) if f.endswith('.nii.gz')]

    # Compute minimal bounding box
    min_bounds, max_bounds = compute_minimal_bounding_box(image_files)

    # Crop and save the images
    crop_and_save_images(image_files, min_bounds, max_bounds, args.output)

if __name__ == '__main__':
    main()