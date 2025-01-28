mkdir checkpoints
mkdir data

python scripts/convert_to_h5.py --input "$HOME/workspace/MSSEG-1-preprocessed-2/" --output "MSSEG-1-preprocessed-2-h5"

mkdir -p "data/train"
mkdir -p "data/val"

FILES=("MSSEG-1-preprocessed-2-h5"/*)

TOTAL_FILES=${#FILES[@]}
COUNT_20=$((TOTAL_FILES / 5)) # 20%
COUNT_80=$((TOTAL_FILES - COUNT_20))

# Shuffle the files
shuf_files=($(shuf -e "${FILES[@]}"))

# Move the first 20%
for i in $(seq 0 $((COUNT_20 - 1))); do
  mv "${shuf_files[$i]}" "data/val"
done

# Move the remaining 80%
for i in $(seq $COUNT_20 $((TOTAL_FILES - 1))); do
  mv "${shuf_files[$i]}" "data/train"
done

echo "Prepare successful"
