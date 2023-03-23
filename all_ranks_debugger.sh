#!/bin/bash

#the prefixes should match how your dataset files are named
percentage_prefix="10"
labels_divider_perfix="50"
labels_seqs_divider_prefix="50"
directory=results/full_datasets_fixed
dataset_name=fixed_

for rank in phylum class order family genus species
do
python dataset_debugger.py $rank $dataset_name
echo REALITY FOR $percentage_prefix%:
grep '>' $directory/training_${percentage_prefix}-percent-${rank}.txt | wc -l
echo REALITY FOR $labels_divider_perfix%
grep '>' $directory/training_${labels_divider_perfix}-${labels_seqs_divider_prefix}-${rank}.txt | wc -l
echo ----------------
done
