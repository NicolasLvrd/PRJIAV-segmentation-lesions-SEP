import argparse

import SimpleITK as sitk


def subtract_segmentations(t1_path, t0_path, output_path):
    """
    Subtracts a segmentation image t0 from t1 and saves the result.

    Parameters:
        t1_path (str): Path to the t1 segmentation image (NIfTI format).
        t0_path (str): Path to the t0 segmentation image (NIfTI format).
        output_path (str): Path to save the resulting image.
    """
    # Load the images
    t1_image = sitk.ReadImage(t1_path)
    t0_image = sitk.ReadImage(t0_path)

    # Ensure the images have the same size and spacing
    if t1_image.GetSize() != t0_image.GetSize():
        raise ValueError("The input images must have the same dimensions.")
    if t1_image.GetSpacing() != t0_image.GetSpacing():
        raise ValueError("The input images must have the same spacing.")

    # Convert images to binary masks
    t1_binary = sitk.BinaryThreshold(t1_image, lowerThreshold=1, upperThreshold=sitk.sitkUInt16, insideValue=1, outsideValue=0)
    t0_binary = sitk.BinaryThreshold(t0_image, lowerThreshold=1, upperThreshold=sitk.sitkUInt16, insideValue=1, outsideValue=0)

    # Subtract t0 from t1
    result_binary = sitk.And(t1_binary, sitk.Not(t0_binary))

    # Multiply result by original t1 to retain original labels
    result_image = sitk.Mask(t1_image, result_binary)

    # Save the resulting image
    sitk.WriteImage(result_image, output_path)


def smart_segmentations(t1_path, t0_path, output_path):
    # Load the input images
    t1 = sitk.ReadImage(t1_path)
    t0 = sitk.ReadImage(t0_path)

    # Ensure the images are in the same space and size
    if t1.GetSize() != t0.GetSize() or t1.GetSpacing() != t0.GetSpacing():
        raise ValueError("Input images must have the same size and spacing.")

    # Convert the images to binary (0 or 1)
    t1 = sitk.BinaryThreshold(t1, lowerThreshold=1, upperThreshold=1, insideValue=1, outsideValue=0)
    t0 = sitk.BinaryThreshold(t0, lowerThreshold=1, upperThreshold=1, insideValue=1, outsideValue=0)

    # Identify connected components in t1 and t0
    t1_components = sitk.ConnectedComponent(t1)
    t0_components = sitk.ConnectedComponent(t0)

    # Get the number of components in t1
    num_components_t1 = sitk.GetArrayViewFromImage(t1_components).max() + 1

    # Create an empty image to store the result
    result = sitk.Image(t1.GetSize(), sitk.sitkUInt8)
    result.CopyInformation(t1)

    # Process each component in t1
    for component in range(1, num_components_t1):
        # Create a binary mask for the current component in t1
        t1_mask = sitk.BinaryThreshold(t1_components, lowerThreshold=component, upperThreshold=component, insideValue=1, outsideValue=0)

        # Check for overlap with components in t0
        overlap_mask = sitk.And(t1_mask, t0)

        # If no overlap, keep the component in the result
        if sitk.GetArrayViewFromImage(overlap_mask).sum() == 0:
            result = sitk.Or(result, t1_mask)

    # Save the output image
    sitk.WriteImage(result, output_path)


# Main function to parse arguments and run the script
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Subtract one NIfTI image from another.")
    parser.add_argument("t0", help="Path to the first NIfTI image (minuend).")
    parser.add_argument("t1", help="Path to the second NIfTI image (subtrahend).")
    parser.add_argument("output", help="Path to save the resulting NIfTI image.")
    parser.add_argument("--mode", default="new_and_grown", help="Mode to compute the new lesion. Default is new_and_grown. Options: new_and_grown (new lesion and the area of lesion that have grown), new (only new lesion).")
    args = parser.parse_args()

    if args.mode == "new_and_grown":
        subtract_segmentations(args.t1, args.t0, args.output)
    elif args.mode == "new":
        smart_segmentations(args.t1, args.t0, args.output)

    print(f"Result saved to {args.output}")
