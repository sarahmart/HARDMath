#!/bin/bash
#SBATCH -p gpu             # Partition to submit to
#SBATCH -t 4:00:00              # Maximum runtime
#SBATCH --cpus-per-task=2                    # Number of CPU cores
#SBATCH --mem=8G                # Total memory
#SBATCH --gres=gpu:teslaV100:1    # Request GPUs
#SBATCH --gres-flags=enforce-binding
#SBATCH --mail-type=ALL                    # ALL email notification type
#SBATCH --mail-user=jfan@g.harvard.edu  # Email to which notifications will be sent

/n/cluster/bin/job_gpu_monitor.sh &
singularity exec --nv /n/app/singularity/containers/shared/ollama-0.1.37.sif ollama serve
