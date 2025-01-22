source "$(dirname "$0")/../constants.sh"

export DATASET_ID=15
export DATASET_NAME=MSSEG1_Full
export DATASET_CONFIG=3d_fullres
export DATASET_PLANER=nnUNetPlannerResEncL # Default Value: "ExperimentPlanner"
export DATASET_PLAN=nnUNetResEncUNetMPlans   # Default Value: "nnUNetPlans"
