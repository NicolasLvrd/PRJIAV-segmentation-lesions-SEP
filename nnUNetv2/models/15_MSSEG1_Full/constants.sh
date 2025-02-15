source "$(dirname "$(realpath "${BASH_SOURCE[0]}")")/../../constants.sh"
export nnUNet_raw nnUNet_preprocessed nnUNet_results INPUT_FILES_ROOT

DATASET_ID=015
DATASET_NAME=MSSEG1_Full
DATASET_CONFIG=3d_fullres
DATASET_PLANER=nnUNetPlannerResEncM # Default Value: "ExperimentPlanner"
DATASET_PLAN=nnUNetResEncUNetMPlans   # Default Value: "nnUNetPlans"
DATASET_PREDICT_FOLD=all # to use only fold 0, set to 0 instead of "all"

export DATASET_ID DATASET_NAME DATASET_CONFIG DATASET_PLANER DATASET_PLAN DATASET_PREDICT_FOLD