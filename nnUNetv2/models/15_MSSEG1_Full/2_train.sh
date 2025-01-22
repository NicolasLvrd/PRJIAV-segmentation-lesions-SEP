source "$(dirname "$0")/constants.sh"

nnUNetv2_train "$DATASET_ID" "$DATASET_CONFIG" 0 -p "$DATASET_PLAN"