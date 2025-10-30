#!/bin/bash
#SBATCH --job-name=sg200080
#SBATCH --output=_log/sg200080-%j.out
#SBATCH --error=_log/sg200080-%j.err
#SBATCH --partition=agent-long
#SBATCH --nodes=1
#SBATCH --gres=gpu:h200:4
#SBATCH --cpus-per-task=40
#SBATCH --mem=400G
#SBATCH --time=3-00:00:00

echo "SLURM_JOB_ID=${SLURM_JOB_ID:-N/A}"
echo "HOSTNAME=$(hostname)"
nvidia-smi || true

for i in {1..5}; do
echo "Run ${i}/5"
python pipeline_local.py --show-progress
done