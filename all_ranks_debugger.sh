#!/bin/bash

#the prefixes should match how your dataset files are named
percentage_prefix="10"
labels_divider_perfix="50"
labels_seqs_divider_prefix="50"

for rank in phylum class order family genus species
do
python dataset_debugger.py $rank
echo REALITY FOR $percentage_prefix%:
grep '>' results/full_datasets_Prokaryotes/training_${percentage_prefix}-percent-${rank}.txt | wc -l
echo REALITY FOR $labels_divider_perfix%
grep '>' results/full_datasets_Prokaryotes/training_${labels_divider_perfix}-${labels_seqs_divider_prefix}-${rank}.txt | wc -l
echo ----------------
done