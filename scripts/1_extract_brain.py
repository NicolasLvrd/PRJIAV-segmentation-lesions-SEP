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

def chunk_list(lst, chunk_size):
    """Yield successive chunks from lst of size chunk_size."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help='Input directory', required=True)
    parser.add_argument('--output', type=str, help='Output directory', required=True)
    args = parser.parse_args()

    maybe_download_parameters()  # Download the model weights

    # find all set of files in the format "number_consensus.nii.gz" and "number_flair_0.nii.gz" and optionally "number_flair_1.nii.gz"
    files_to_process = []
    for file in os.listdir(args.input):
        if file.endswith('.nii.gz'):
            if file.endswith('consensus.nii.gz'):
                number = file.split('_')[0]
                flair_0 = os.path.join(args.input, f'{number}_flair_0.nii.gz')
                flair_1 = os.path.join(args.input, f'{number}_flair_1.nii.gz')

                if os.path.exists(flair_0):
                    os.makedirs(args.output, exist_ok=True)
                    shutil.copy(os.path.join(args.input, file), os.path.join(args.output, file))
                    files_to_process.append((flair_0, os.path.join(args.output,  f'{number}_flair_0.nii.gz')))

                    if os.path.exists(flair_1):
                        files_to_process.append((flair_1, os.path.join(args.output, f'{number}_flair_1.nii.gz')))

    for chunk in chunk_list(files_to_process, 20):
        hdbet_predict_custom(chunk, keep_brain_mask=False, compute_brain_extracted_image=True)


if __name__ == '__main__':
    main()
