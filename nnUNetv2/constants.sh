nnUNet_raw="$(dirname "$(realpath "${BASH_SOURCE[0]}")")/nnunet_internal/datasets"
nnUNet_preprocessed="$(dirname "$(realpath "${BASH_SOURCE[0]}")")/nnunet_internal/preprocessed"
nnUNet_results="$(dirname "$(realpath "${BASH_SOURCE[0]}")")/nnunet_internal/results"
INPUT_FILES_ROOT="$HOME/workspace"

export nnUNet_raw nnUNet_preprocessed nnUNet_results INPUT_FILES_ROOT