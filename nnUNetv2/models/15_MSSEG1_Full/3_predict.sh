source "$(dirname "$(realpath "${BASH_SOURCE[0]}")")/constants.sh"

rm -f "${nnUNet_raw}/Dataset${DATASET_ID}_${DATASET_NAME}/predictTs/*"

nnUNetv2_predict -i "${nnUNet_raw}/Dataset${DATASET_ID}_${DATASET_NAME}/imagesTs/" \
    -o "${nnUNet_raw}/Dataset${DATASET_ID}_${DATASET_NAME}/predictTs" \
    -d "$DATASET_ID" \
    -c "$DATASET_CONFIG" \
    -chk checkpoint_best.pth \
    -p "$DATASET_PLAN"