import argparse
import os
import shutil


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help='Input directory', required=True)
    parser.add_argument('--output', type=str, help='Output directory', required=True)
    parser.add_argument('--database-type', type=str, help='Type of database', choices=['MSSEG-1', 'MSSEG-1-test', 'MSSEG-2'], required=True)
    args = parser.parse_args()

    if args.database_type == 'MSSEG-1':
        flair_file_name = ['3DFLAIR.nii']
        consensus_file_name = 'Consensus.nii'
    elif args.database_type == 'MSSEG-1-test':
        flair_file_name = ['3DFLAIR.nii.gz']
        consensus_file_name = 'Consensus.nii.gz'
    else:
        flair_file_name = ['flair_time01_on_middle_space.nii.gz', 'flair_time02_on_middle_space.nii.gz']
        consensus_file_name = 'ground_truth.nii.gz'

    for root, dirs, files in os.walk(args.input):
        if consensus_file_name in files and all([flair in files for flair in flair_file_name]):
            identifier = ''.join(filter(lambda x: x.isdigit(), os.path.basename(root)))
            for i, flair in enumerate(flair_file_name):
                output_file = os.path.join(args.output, f'{identifier}_flair_{i}.nii.gz')
                os.makedirs(os.path.dirname(output_file), exist_ok=True)

                shutil.copy(os.path.join(root, flair), output_file)

            shutil.copy(os.path.join(root, consensus_file_name), args.output + f'/{identifier}_consensus.nii.gz')

if __name__ == '__main__':
    main()
