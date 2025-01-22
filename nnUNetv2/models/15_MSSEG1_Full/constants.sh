source "$(dirname "$(realpath "${BASH_SOURCE[0]}")")/../../constants.sh"
export nnUNet_raw nnUNet_preprocessed nnUNet_results

DATASET_ID=015
DATASET_NAME=MSSEG1_Full
DATASET_CONFIG=3d_fullres
DATASET_PLANER=nnUNetPlannerResEncM # Default Value: "ExperimentPlanner"
DATASET_PLAN=nnUNetResEncUNetMPlans   # Default Value: "nnUNetPlans"

export DATASET_ID DATASET_NAME DATASET_CONFIG DATASET_PLANER DATASET_PLAN