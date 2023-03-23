import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="Get numbers for ranks")
parser.add_argument('rank', type=str, help="index of sequence to start finding rank numbers")
parser.add_argument('prefix', type=str, help="index of sequence to start finding rank numbers")
args = parser.parse_args()

rank=str(args.rank)
prefix=str(args.prefix)

ref_file=pd.read_csv('results/seqs_per_rank/'+prefix+'seqs_for_each_'+rank+'.csv')

tens=[int(x/10) for x in ref_file.iloc[:,1] if x >= 10]

print('there should be '+ str(sum(tens)) + ' sequences in the '+ rank +' 10% training dataset')

with open('results/chosen_50/'+ rank + '_chosen_half.txt') as f:
    ref_2=f.read().splitlines()
twos=[int(ref_file.iloc[x,1]/2) for x in range(0,len(ref_file.iloc[:,1])) if ref_file.iloc[x,1] >=2 and ref_file.iloc[x,0] in ref_2]
print('there should be '+ str(sum(twos)) + ' sequences in the '+ rank +' 50% training dataset')


# file=pd.read_csv('/ifs/groups/rosenMRIGrp/jv545/DeepLearning/qiime_tutorial/jv545_work/Silva/ncbi_work/results/all_tax_ids.csv')
# print('yooo')
