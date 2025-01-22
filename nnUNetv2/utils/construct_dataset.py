import os
import random
import shutil
from glob import glob

import argparse
from pathlib import Path

from nnunetv2.dataset_conversion.generate_dataset_json import generate_dataset_json
from nnunetv2.paths import nnUNet_raw


def prepare_folders(output_dir: Path):
    # Cleanup
    if os.path.exists(output_dir / 'imagesTr'): shutil.rmtree(output_dir / 'imagesTr')
    if os.path.exists(output_dir / 'imagesTs'): shutil.rmtree(output_dir / 'imagesTs')
    if os.path.exists(output_dir / 'labelsTr'): shutil.rmtree(output_dir / 'labelsTr')
    if os.path.exists(output_dir / 'labelsTs'): shutil.rmtree(output_dir / 'labelsTs')

    # Create folders
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(output_dir / 'imagesTr', exist_ok=True)
    os.makedirs(output_dir / 'imagesTs', exist_ok=True)
    os.makedirs(output_dir / 'labelsTr', exist_ok=True)
    os.makedirs(output_dir / 'labelsTs', exist_ok=True)


def main(input_dirs: list[Path], output_dir: Path, test_percentage: float, flair_count: int):
    prepare_folders(output_dir)

    # Get files
    flair_files = [
        sorted(file for data_dir in input_dirs for file in glob(os.path.join(data_dir, f'*_flair_{i}.nii.gz')))
        for i in range(flair_count)
    ]
    consensus_files = sorted(
        file for data_dir in input_dirs for file in glob(os.path.join(data_dir, '*_consensus.nii.gz'))
    )
    files = list(zip(*flair_files, consensus_files))

    # Randomize order
    random.shuffle(files)

    # Copy files
    files_mapping = {}
    nb_train = int(len(files) * (1 - test_percentage))
    for i, file_set in enumerate(files):
        consensus_file = file_set[-1]
        consensus_new_name = f"img_{i + 1:03d}.nii.gz"
        if i < nb_train:
            shutil.copy(consensus_file, output_dir / 'labelsTr' / consensus_new_name)
        else:
            shutil.copy(consensus_file, output_dir / 'labelsTs' / consensus_new_name)
        files_mapping[consensus_file] = consensus_new_name

        for j, flair_file in enumerate(file_set[:-1]):
            flair_new_name = f"img_{i + 1:03d}_{j:04d}.nii.gz"
            if i < nb_train:
                shutil.copy(flair_file, output_dir / 'imagesTr' / flair_new_name)
            else:
                shutil.copy(flair_file, output_dir / 'imagesTs' / flair_new_name)
            files_mapping[flair_file] = flair_new_name

    # Save files naming map
    with open(output_dir / 'files_mapping.txt', 'w') as f:
        for k, v in files_mapping.items():
            f.write(f"{os.path.basename(k)} -> {v}\n")

    generate_dataset_json(output_folder=str(output_dir),
                          channel_names={i: f"flair" for i in range(flair_count)},
                          labels={
                              "background": 0,
                              "consensus": 1
                          },
                          num_training_cases=nb_train,
                          dataset_name=output_dir.name,
                          file_ending='.nii.gz',
                          overwrite_image_reader_writer="SimpleITKIO",
                          )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, nargs='+', help='Input directories', required=True)
    parser.add_argument('--dataset-id', type=int, help='Dataset id', required=True)
    parser.add_argument('--dataset-name', type=str, help='Dataset name', required=True)
    parser.add_argument('--test-percentage', type=float, help='Percentage of test data', default=0.2)
    parser.add_argument('--flair-count', type=int, help='Number of FLAIR files', default=1)
    args = parser.parse_args()

    main([Path(input_dir) for input_dir in args.input], Path(nnUNet_raw) / f"Dataset{args.dataset_id:03d}_{args.dataset_name}", args.test_percentage, args.flair_count)
