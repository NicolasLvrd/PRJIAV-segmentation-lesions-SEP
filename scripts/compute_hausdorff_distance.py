import argparse

import SimpleITK as sitk


def compute_hausdorff_distance(mask1_path, mask2_path):
    """
    Compute the Hausdorff distance between two binary segmentation masks.

    :param mask1_path: Path to the first binary mask (NIfTI, DICOM, etc.).
    :param mask2_path: Path to the second binary mask.
    :return: Hausdorff distance value.
    """
    # Load binary masks
    mask1 = sitk.ReadImage(mask1_path)
    mask2 = sitk.ReadImage(mask2_path)

    spacing1 = mask1.GetSpacing()
    spacing2 = mask2.GetSpacing()
    print(f"Image 1 Spacing: {spacing1}")
    print(f"Image 2 Spacing: {spacing2}")


    # Compute Hausdorff distance
    hausdorff_filter = sitk.HausdorffDistanceImageFilter()
    hausdorff_filter.Execute(mask1, mask2)

    return hausdorff_filter.GetHausdorffDistance()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--consensus', type=str, help='Path to the first binary mask', required=True)
    parser.add_argument('--prediction', type=str, help='Path to the second binary mask', required=True)
    args = parser.parse_args()

    hausdorff_distance = compute_hausdorff_distance(args.consensus, args.prediction)
    print(f"Hausdorff Distance: {hausdorff_distance}")
