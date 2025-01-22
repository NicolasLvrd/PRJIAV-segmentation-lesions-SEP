source "$(dirname "$0")/constants.sh"

python "$(dirname "$0")/../../utils/construct_dataset.py" \
    --input "$HOME/workspace/MSSEG-1-preprocessed-2"\
    --input "$HOME/workspace/MSSEG-1-test-preprocessed-2" \
    --dataset-id "$DATASET_ID" \
    --dataset-name "$DATASET_NAME"