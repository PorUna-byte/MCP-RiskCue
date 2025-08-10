#!/bin/bash
#SBATCH --job-name=dr-test
#SBATCH --output=_log/test-%j.out
#SBATCH --error=_log/test-%j.err
#SBATCH --partition=h100-agent-train
#SBATCH --nodelist=lrc-alpha-gpu10
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=2
#SBATCH --mem=10G
#SBATCH --time=00:10:00

echo "SLURM_JOB_ID=$SLURM_JOB_ID"
echo "HOSTNAME=$(hostname)"
nvidia-smi          # 查看 GPU 状态
python test.py            # print("hello world") for 1000 times

