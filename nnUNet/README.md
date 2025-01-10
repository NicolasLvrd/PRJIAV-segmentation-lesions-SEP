## Configuration

1. Install requirements
```
pip install -r requirements.txt
```
2. Set environment variables
    - Make a copy of constants.sh.example
    - Rename to constants.sh
    - Set the 3 environment variables with the actual folders you intend to use

## Execution
```
source constants.sh
```
Run preprocessing
```
nnUNetv2_plan_and_preprocess -d 11 --verify_dataset_integrity
```
Run training
```
nnUNetv2_train 11 3d_fullres 0
```