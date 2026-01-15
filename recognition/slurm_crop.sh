#!/bin/bash
#SBATCH --job-name=crop_dr
#SBATCH --partition=gpu-l40s
#SBATCH --account=gbru
#SBATCH --qos=normal
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=24:00:00
#SBATCH --output=cropdr_%j.out
#SBATCH --error=cropdr_%j.err


# 1. Define Absolute Paths
SUBMIT_DIR=$(pwd)
# DATADIR="input_images" #test folder
DATADIR="captured_images2_inverted"
# Use a job-specific scratch folder to avoid collisions
SCRATCH_INPUT="$TMPDIR/job_input"
SCRATCH_OUTPUT="$TMPDIR/job_output"

mkdir -p "$SCRATCH_INPUT" "$SCRATCH_OUTPUT"

# 2. Transfer Data (Note the trailing slash on source)
echo "Syncing data to local scratch..."
rsync -aW "${SUBMIT_DIR}/${DATADIR}/" "$SCRATCH_INPUT/"

# 3. Setup Environment
module purge
module load cuda/12.9.0 miniconda3
source activate /project/gbru_fy21_therm_mastitis/ocrdoctr_env

# 4. Run Inference
echo "Starting cropping from $SCRATCH_INPUT to $SCRATCH_OUTPUT"
# Use -u to ensure Python output is not buffered in the SLURM log
python -u crop_training_images.py --input "$SCRATCH_INPUT" --output "$SCRATCH_OUTPUT"

# 5. CRITICAL: Copy results back to persistent storage
echo "Transferring results back to $SUBMIT_DIR..."
rsync -aW "$SCRATCH_OUTPUT/" "${SUBMIT_DIR}/cropped_images2_inverted/"

echo "Job complete."