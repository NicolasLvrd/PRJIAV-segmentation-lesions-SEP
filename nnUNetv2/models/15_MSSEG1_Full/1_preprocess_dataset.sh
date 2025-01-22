source "$(dirname "$0")/constants.sh"

nnUNetv2_plan_and_preprocess -d "$DATASET_ID" --verify_dataset_integrity -pl "$DATASET_PLANER"