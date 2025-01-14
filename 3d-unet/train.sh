mkdir checkpoints
mkdir data

python scripts/convert_to_h5.py


train3dunet --config train_config.yml