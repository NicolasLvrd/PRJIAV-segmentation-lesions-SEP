source "$(dirname "$(realpath "${BASH_SOURCE[0]}")")/../../constants.sh"

DATASET_ID=15
DATASET_NAME=MSSEG1_Full
DATASET_CONFIG=3d_fullres
DATASET_PLANER=nnUNetPlannerResEncL # Default Value: "ExperimentPlanner"
DATASET_PLAN=nnUNetResEncUNetLPlans   # Default Value: "nnUNetPlans"

export DATASET_ID DATASET_NAME DATASET_CONFIG DATASET_PLANER DATASET_PLAN nnUNet_raw nnUNet_preprocessed nnUNet_results