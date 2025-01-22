source "$(dirname "$(realpath "${BASH_SOURCE[0]}")")/constants.sh"

nnUNetv2_evaluate_folder "${nnUNet_raw}/Dataset${DATASET_ID}_${DATASET_NAME}/labelTs/" \
    "${nnUNet_raw}/Dataset${DATASET_ID}_${DATASET_NAME}/predictTs" \
    -djfile "${nnUNet_raw}/Dataset${DATASET_ID}_${DATASET_NAME}/dataset.json" \
    -pfile "${nnUNet_results}/Dataset${DATASET_ID}_${DATASET_NAME}/plans.json"