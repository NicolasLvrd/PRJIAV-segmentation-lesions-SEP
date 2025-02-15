source "$(dirname "$(realpath "${BASH_SOURCE[0]}")")/constants.sh"

python "$(dirname "$(realpath "${BASH_SOURCE[0]}")")/../../utils/construct_dataset.py" \
    --input "$INPUT_FILES_ROOT/MSSEG-1-preprocessed-2" \
    --input "$INPUT_FILES_ROOT/MSSEG-1-test-preprocessed-2" \
    --dataset-id "$DATASET_ID" \
    --dataset-name "$DATASET_NAME"