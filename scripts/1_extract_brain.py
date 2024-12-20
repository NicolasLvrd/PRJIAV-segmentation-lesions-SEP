import os
import shutil
from multiprocessing import Pool

import torch
from HD_BET.checkpoint_download import maybe_download_parameters
from HD_BET.hd_bet_prediction import get_hdbet_predictor, apply_bet
import argparse


def hdbet_predict_custom(
        files: list[tuple[str, str]],
        keep_brain_mask: bool = False,
        compute_brain_extracted_image: bool = True
):
    predictor = get_hdbet_predictor(
        use_tta=True if torch.cuda.is_available() else False,  # Use test time augmentation only if a GPU is available
        device=torch.device('cuda' if torch.cuda.is_available() else 'cpu'),  # Use GPU if available, otherwise use CPU
        verbose=False
    )

    input_files = [i[0] for i in files]
    output_files = [i[1] for i in files]
    brain_mask_files = [i[:-7] + '_bet.nii.gz' for i in output_files]

    # we first just predict the brain masks using the standard nnU-Net inference
    predictor.predict_from_files(
        [[i] for i in input_files],
        brain_mask_files,
        save_probabilities=False,
        overwrite=True,
        num_processes_preprocessing=4,
        num_processes_segmentation_export=8,
        folder_with_segs_from_prev_stage=None,
        num_parts=1,
        part_id=0
    )
    # remove unnecessary json files
    os.remove(os.path.join(os.path.dirname(brain_mask_files[0]), 'dataset.json'))
    os.remove(os.path.join(os.path.dirname(brain_mask_files[0]), 'plans.json'))
    os.remove(os.path.join(os.path.dirname(brain_mask_files[0]), 'predict_from_raw_data_args.json'))

    if compute_brain_extracted_image:
        # now brain extract the images
        res = []
        with Pool(4) as p:
            for im, bet, out in zip(input_files, brain_mask_files, output_files):
                res.append(
                    p.starmap_async(
                        apply_bet,
                        ((im, bet, out),)
                    )
                )
            [i.get() for i in res]

    if not keep_brain_mask:
        [os.remove(i) for i in brain_mask_files]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help='Input directory', required=True)
    parser.add_argument('--output', type=str, help='Output directory', required=True)
    parser.add_argument('--database-type', type=str, help='Type of database', choices=['MSSEG-1', 'MSSEG-2'], required=True)
    args = parser.parse_args()

    if args.database_type == 'MSSEG-1':
        flair_file_name = ['3DFLAIR.nii']
        consensus_file_name = 'Consensus.nii'
    else:
        flair_file_name = ['flair_time01_on_middle_space.nii.gz', 'flair_time02_on_middle_space.nii.gz']
        consensus_file_name = 'ground_truth.nii.gz'

    maybe_download_parameters()  # Download the model weights

    files_to_process = []
    for root, dirs, files in os.walk(args.input):
        if consensus_file_name in files and all([flair in files for flair in flair_file_name]):
            identifier = ''.join(filter(lambda x: x.isdigit(), os.path.basename(root)))
            for i, flair in enumerate(flair_file_name):
                input_file = os.path.join(root, flair)
                output_file = os.path.join(args.output, f'{identifier}_flair_{i}.nii.gz')
                os.makedirs(os.path.dirname(output_file), exist_ok=True)

                files_to_process.append((input_file, output_file))

            shutil.copy(os.path.join(root, consensus_file_name), args.output + f'/{identifier}_consensus.nii.gz')

    hdbet_predict_custom(files_to_process, keep_brain_mask=True, compute_brain_extracted_image=True)


if __name__ == '__main__':
    main()
