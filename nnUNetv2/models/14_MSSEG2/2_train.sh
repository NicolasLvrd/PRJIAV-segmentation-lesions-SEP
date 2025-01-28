source "$(dirname "$(realpath "${BASH_SOURCE[0]}")")/constants.sh"

if [ -z "$1" ]; then
  echo "Please provide the fold number as an argument (between 0 and 4)."
  exit 1
fi
FOLD=$1

nnUNetv2_train "$DATASET_ID" "$DATASET_CONFIG" "$FOLD" -p "$DATASET_PLAN"