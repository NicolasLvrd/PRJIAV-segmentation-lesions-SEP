import argparse
import os

import SimpleITK as sitk
import h5py


def process_file(nii_file_path, consensus_file_path, h5_file_path):
    image = sitk.ReadImage(nii_file_path)
    image_array = sitk.GetArrayFromImage(image)

    consensus = sitk.ReadImage(consensus_file_path)
    consensus_array = sitk.GetArrayFromImage(consensus)

    spacing = image.GetSpacing()
    origin = image.GetOrigin()
    direction = image.GetDirection()

    # Save the data to an HDF5 file
    with h5py.File(h5_file_path, "w") as h5_file:
        # Save the image data
        h5_file.create_dataset("raw", data=image_array, compression="gzip")
        h5_file.create_dataset("label", data=consensus_array, compression="gzip")

        # Save metadata as attributes
        h5_file.attrs["spacing"] = spacing
        h5_file.attrs["origin"] = origin
        h5_file.attrs["direction"] = direction

    print(f"Converted {nii_file_path} to {h5_file_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help='Input directory', required=True)
    parser.add_argument('--output', type=str, help='Output directory', required=True)
    args = parser.parse_args()

    # find all set of files in the format "number_consensus.nii.gz" and "number_flair_0.nii.gz" and optionally "number_flair_1.nii.gz"
    files_to_process = []
    for file in os.listdir(args.input):
        if file.endswith('consensus.nii.gz'):
            number = file.split('_')[0]
            flair_0 = os.path.join(args.input, f'{number}_flair_0.nii.gz')
            flair_1 = os.path.join(args.input, f'{number}_flair_1.nii.gz')

            if os.path.exists(flair_0):
                os.makedirs(args.output, exist_ok=True)
                files_to_process.append((flair_0, os.path.join(args.input, file), os.path.join(args.output,  f'{number}_flair_0.h5')))

                if os.path.exists(flair_1):
                    files_to_process.append((flair_1, os.path.join(args.output, f'{number}_flair_1.h5')))

    for nii_file_path, consensus_file_path, h5_file_path in files_to_process:
        process_file(nii_file_path, consensus_file_path, h5_file_path)


if __name__ == '__main__':
    main()
