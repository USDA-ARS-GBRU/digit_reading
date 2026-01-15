#!/bin/bash
#SBATCH --job-name=doctr-crnn
#SBATCH --partition=gpu-l40s
#SBATCH --account=gbru
#SBATCH --qos=normal
#SBATCH --nodes=1
#SBATCH --gres=gpu:4
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=11:00:00
#SBATCH --output=doctr_rec_%j.out
#SBATCH --error=doctr_rec_%j.err

echo "Starting job on $SLURM_NODELIST"
echo "SLURM_JOBID: $SLURM_JOB_ID"

# 1. Load Environment
module purge
module load cuda/12.9.0
module load miniconda3
source activate /project/gbru_fy21_therm_mastitis/ocrdoctr_env

# 2. Paths & Scratch Setup
PROJECT_DIR="/project/gbru_fy21_therm_mastitis/ocr/recognition"
TRAIN_SRC="train_path"   # CHANGE THIS
VAL_SRC="val_path"       # CHANGE THIS

# Define Local Scratch Paths
LOCAL_TRAIN="$TMPDIR/train_data"
LOCAL_VAL="$TMPDIR/val_data"
LOCAL_MODELS="$TMPDIR/saved_models"

mkdir -p "$LOCAL_TRAIN" "$LOCAL_VAL" "$LOCAL_MODELS"

# 3. RSYNC DATA TO NODE (Crucial for performance)
# The trailing slash "/" copies the contents of the directory
echo "Syncing data to local scratch: $TMPDIR"
rsync -aW "${TRAIN_SRC}/" "$LOCAL_TRAIN/"
rsync -aW "${VAL_SRC}/" "$LOCAL_VAL/"

echo "Data sync complete."

# 4. Launch RECOGNITION training
# -u forces unbuffered output so you see your Batch N/Total N lines instantly
echo "Starting recognition training on 4x L40S"

torchrun \
  --nproc_per_node=4 \
  /project/gbru_fy21_therm_mastitis/ocr/doctr/references/recognition/train.py crnn_mobilenet_v3_large \
    --train_path "$LOCAL_TRAIN" \
    --val_path "$LOCAL_VAL" \
    --output_dir "$LOCAL_MODELS" \
    --vocab "digits" \
    --epochs 30 \
    --batch_size 256 \
    --workers 4 \
    --lr 0.0002 \
    --optim adamw \
    --sched cosine \
    --amp \
    --early-stop \
    --early-stop-epochs 5 \
    --wd 0.02

# 5. SYNC MODELS BACK TO PROJECT
echo "Training complete. Copying models back to permanent storage."
rsync -av "$LOCAL_MODELS/" "${PROJECT_DIR}/saved_models/"
