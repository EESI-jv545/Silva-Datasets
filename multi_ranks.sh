#!/bin/bash
#SBATCH --account=rosenMRIPrj
#SBATCH --mail-user=jv545@drexel.edu
#SBATCH --cpus-per-task=1
#SBATCH -t 2:00:00
#SBATCH --partition=def
#SBATCH --mem=500M
#SBATCH --array=0-51%15
#SBATCH --output=/ifs/groups/rosenMRIGrp/jv545/DeepLearning/qiime_tutorial/jv545_work/Silva/ncbi_work/slurm-out/species-ranks-%A_%a.out
#SBATCH --error=/ifs/groups/rosenMRIGrp/jv545/DeepLearning/qiime_tutorial/jv545_work/Silva/ncbi_work/slurm-out/species-ranks-%A_%a.err

. ~/.bashrc

# region=V1V9
# primers=27F_1492R

source /ifs/groups/rosenMRIGrp/pythonenv/SILVA-env/bin/activate

python find_ranks.py $SLURM_ARRAY_TASK_ID /scratch/jv545/ncbi/ /ifs/groups/rosenMRIGrp/jv545/DeepLearning/qiime_tutorial/jv545_work/Silva/all-sequences-names.txt tax_ncbi-species_ssu_ref_138.1.txt

# mv $sample GNUVID_results/
echo done!
