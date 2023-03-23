import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="Get numbers for ranks")
parser.add_argument('start', type=str, help="index of sequence to start finding rank numbers")
parser.add_argument('output', type=str, help="output directory to store groups of sequences")
parser.add_argument('names_input', type=str, help="pathway to the names of the Silva sequences")
parser.add_argument('tax_map', type=str, help="pathway to the file that maps Silva seqs to taxIDs")
args = parser.parse_args()

#assigns taxIDs to every 10000 sequences
start=int(args.start)*10000
end=start+10000

output=str(args.output)
names_file=str(args.names_input)
tax_map=str(args.tax_map)
#------------End of user Inputs-----------

print(str(start), flush=True)

print('reading sequence names', flush=True)
with open(names_file) as f:
    seq_names=f.read().splitlines()

print('reading tax file', flush=True)
# lines=pd.read_csv('/ifs/groups/rosenMRIGrp/jv545/DeepLearning/qiime_tutorial/jv545_work/Silva/ncbi_work/tax_ncbi_ssu_ref_138.1.txt', sep='\t', header=None)
lines=pd.read_csv(tax_map, sep='\t', header=None)
names=list(lines.iloc[:,0])

if len(seq_names)<end:
    end=len(seq_names)

#start to assign taxIDs to sequences
print('starting!', flush=True)
ranks_dict={}
for i in seq_names[start:end]:
    print(str(seq_names.index(i)) + '------> ' + i, flush=True)
    number=[]
    spot=1 #starting at the lowest rank (species) and seeing if it has a taxID; if not, work up from there with each run of the while loop
    temp=''
    temp_name=''
    while number==[]:
        rank=i.split(';')[spot*-1]+';'  #the NCBI file has semicolons after each rank label
        if 'phage' in rank or 'uncultured' in rank or 'unclassified' in rank or 'virus' in rank or 'Phage' in rank:
            spot+=1
            continue
        if '>' in rank:
            rank=rank.split(' ')[1]
        for name in names:
            if 'Eukaryota' not in name and 'Archaea' not in name and 'Bacteria' not in name:
                continue
            if rank in name:
                row=names.index(name)
                if lines.iloc[row,2] != 'no rank':
                # if lines.iloc[row,2] == 'phylum' and rank == name.split(';')[-2]:
                    number=lines.iloc[row,1]
                    break
        spot+=1
    if number not in ranks_dict.keys():
        ranks_dict[number]=[]
    ranks_dict[number].append(i)

#make a dataframe of all the taxID assignments
df=pd.DataFrame({'taxID':[], 'sequences':[]})
for i in ranks_dict.keys():
    df=df.append({'taxID':i, 'sequences':ranks_dict[i]},ignore_index=True)
df.to_csv(output+'/'+str(start)+'.csv', index=False)
# df.to_csv('/ifs/groups/rosenMRIGrp/jv545/DeepLearning/qiime_tutorial/jv545_work/Silva/ncbi_work/phage_taxIDs.csv', index=False)
