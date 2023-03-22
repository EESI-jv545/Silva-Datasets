#!/bin/bash
#SBATCH --account=rosenMRIPrj
#SBATCH --mail-user=jv545@drexel.edu
#SBATCH --cpus-per-task=1
#SBATCH -t 48:00:00
#SBATCH --partition=def
#SBATCH --mem=3G
#SBATCH --array=0-9
#SBATCH --output=/ifs/groups/rosenMRIGrp/jv545/DeepLearning/qiime_tutorial/jv545_work/Silva/ncbi_work/slurm-out/general_datasets-%A_%a.out
#SBATCH --error=/ifs/groups/rosenMRIGrp/jv545/DeepLearning/qiime_tutorial/jv545_work/Silva/ncbi_work/slurm-out/general_datasets-%A_%a.err

. ~/.bashrc

# region=V1V9
# primers=27F_1492R

# mkdir -p /scratch/jv545/DAIRYdb/$region

source /ifs/groups/rosenMRIGrp/pythonenv/SILVA-env/bin/activate

python general-make_datasets.py $SLURM_ARRAY_TASK_ID results/full_datasets_fixed

# mv $sample GNUVID_results/
echo done!


