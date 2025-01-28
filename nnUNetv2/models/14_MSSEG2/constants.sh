source "$(dirname "$(realpath "${BASH_SOURCE[0]}")")/../../constants.sh"
export nnUNet_raw nnUNet_preprocessed nnUNet_results INPUT_FILES_ROOT

DATASET_ID=014
DATASET_NAME=MSSEG2
DATASET_CONFIG=2d
DATASET_PLANER=ExperimentPlanner
DATASET_PLAN=nnUNetPlans
DATASET_PREDICT_FOLD=all # to use only fold 0, set to 0 instead of "all"

export DATASET_ID DATASET_NAME DATASET_CONFIG DATASET_PLANER DATASET_PLAN DATASET_PREDICT_FOLD