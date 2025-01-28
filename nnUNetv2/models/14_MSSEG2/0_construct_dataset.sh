source "$(dirname "$(realpath "${BASH_SOURCE[0]}")")/constants.sh"

python "$(dirname "$(realpath "${BASH_SOURCE[0]}")")/../../utils/construct_dataset.py" \
    --input "$INPUT_FILES_ROOT/MSSEG-2-preprocessed-2" \
    --dataset-id "$DATASET_ID" \
    --dataset-name "$DATASET_NAME" \
    --flair-count 2