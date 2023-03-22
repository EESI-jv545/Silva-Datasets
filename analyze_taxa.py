from ete3 import NCBITaxa
import pandas as pd
import pdb

#you may need to change these variables depending on how your files are named
input_file='fixed_all_tax_ids.csv'
output='results'
out_file='fixed_all_ids_w_taxonomy.csv'
#----------------End of Inputs-----------------#

csv=pd.read_csv(output+'/'+input_file)

ncbi = NCBITaxa()

#------
full_dataframe=pd.DataFrame({'taxID':[], 'total sequences': [], 'superkingdom':[], 'kingdom':[], 'phylum':[], 'class':[], 'order':[], 'family':[], 'genus':[], 'species':[], 'sequences':[]})
weirds=[]
cats=[]
kingdoms=[]
lost={}
for i in range(0,len(csv.iloc[:,0])):
    print(i/len(csv.iloc[:,0]))
    taxid=int(csv.iloc[i,0])
    # taxid=77133
    ranks_dict={}
    # if i==3:
    #     break
    # taxid=1301
    sequences=csv.loc[i,'sequences']
    total=int(csv.loc[i,'total sequences'])
    # print('TaxID= '+str(taxid))
    try:
        lineage = ncbi.get_lineage(taxid)
    except:
        weirds.append(taxid)
        continue
    # print(lineage)
    
    ranks=ncbi.get_rank(lineage)
    ranks_dict= dict([(value, key) for key, value in ranks.items()])
    # print(ranks_dict.keys())
    # try:
    #     if ranks_dict['superkingdom']=='Viruses' or 'superkingdom' not in ranks_dict.keys():
    #         pdb.set_trace()
    # except:
    #     pdb.set_trace()
    # pdb.set_trace()

    # print(ranks_dict)
    names = ncbi.get_taxid_translator(lineage)
    
#     if 'superkingdom' not in ranks_dict.keys():
#         lost[taxid]=sequences
#     # print([names[taxid] for taxid in lineage])
# with open('lost.txt','w') as f:
#     for key in lost.keys():
#         f.write(str(key))
#         # f.write(': ')
#         # f.write(lost[key])
#         f.write('\n')
# with open('lost_w_seqs.txt','w') as f:
#     for key in lost.keys():
#         f.write(str(key))
#         f.write(': ')
#         f.write(lost[key])
#         f.write('\n')

    # print(taxid)
    ranks_dict['taxID']=taxid
    ranks_dict['total sequences']=total
    # pdb.set_trace()
    ranks_dict['sequences']=sequences
    
    Nones=[x for x in full_dataframe.columns if x not in ranks_dict]
    for i in Nones:
        ranks_dict[i]=None
    # if taxid == 134726:
    
    # full_ranks={}
    row_count=full_dataframe.shape[0]
    full_dataframe.loc[row_count] = [None]*len(full_dataframe.columns)
    # print(list(ranks_dict.keys())[:-1])
    # print(names)

    # kingdom_list=[x for x in ranks_dict.keys() if 'kingdom' in x]
    # if kingdom_list != []:
    # if 'kingdom' in ranks_dict.keys():
    #     if names[ranks_dict['kingdom']] not in kingdoms:
    #         kingdoms.append(names[ranks_dict['kingdom']])

    for j in ranks_dict.keys():
        if ranks_dict[j] == None or j not in full_dataframe.columns:
            if j not in full_dataframe.columns and j not in cats:
                cats.append(j)
            continue
        if j in ['taxID', 'total sequences', 'sequences']:
            full_dataframe.loc[row_count, j] = ranks_dict[j]
            if j == 'sequences' and '\\' in full_dataframe.loc[row_count, j]:
                pdb.set_trace()
        else:
            full_dataframe.loc[row_count, j] = names[ranks_dict[j]]

full_dataframe.to_csv(output+'/'+out_file, index=None)
# full_dataframe.to_csv('results/no_backslash_all_ids_w_taxonomy.csv', index=None)
#-----

# print(kingdoms)
# pdb.set_trace()
# full_dataframe=pd.read_csv('results/'+prefix+'all_ids_w_taxonomy.csv')
# phyla_dict={}
# phyla=full_dataframe['phylum'].unique()
# for p in phyla:
#     print(p)
#     if type(p) == float:
#         continue
#     rows = [i for i, x in enumerate(list(full_dataframe['phylum'])) if x == p]
#     taxid2name = (ncbi.get_name_translator([p]))
#     phylaid=taxid2name[p][0]
#     if phylaid not in phyla_dict.keys():
#         phyla_dict[phylaid]=[0, [], []]
#     for r in rows:
#         print(r)
#         phyla_dict[phylaid][0]+=full_dataframe.loc[r, 'total sequences']
#         seqs=full_dataframe.loc[r, 'sequences'].strip("'[]").split("', '")
#         # pdb.set_trace()
#         seqs_w_p=[x for x in seqs if p in x]
#         print(phyla_dict[phylaid][0])
#         if p not in phyla_dict[phylaid][1]:
#             phyla_dict[phylaid][1].append(p)
#         print(phyla_dict[phylaid][1])
#         # full_seqs=full_dataframe.loc[r, 'sequences'].strip("'[]").split("', '")
#         phyla_dict[phylaid][2]+=full_dataframe.loc[r, 'sequences'].strip("'[]").split("', '")
#         # print('good!')
# phyla_frame=pd.DataFrame({'phylum_id':[], 'total sequences': [], 'phylum name(s)':[], 'sequences':[]})

# for key in phyla_dict.keys():
#     print(list(phyla_dict.keys()).index(key)/len(list(phyla_dict.keys())))
#     row_count=phyla_frame.shape[0]
#     phyla_frame.loc[row_count] = [None]*len(phyla_frame.columns)
#     phyla_frame.loc[row_count, 'phylum_id'] = key
#     phyla_frame.loc[row_count, 'total sequences'] = phyla_dict[key][0]
#     phyla_frame.iloc[row_count, 2] = str(phyla_dict[key][1])
#     phyla_frame.iloc[row_count, 3] = str(phyla_dict[key][2])



# phyla_frame=phyla_frame.sort_values(by='total sequences', ascending=False)
# phyla_frame.to_csv('results/'+prefix+'all_phyla.csv', index=None)


# pdb.set_trace()

# levels_dict={}
# for c in full_dataframe.columns[2:9]:
#     print('------------')
#     print(c)
#     print('------------')
#     uniques=full_dataframe[c].unique()
#     for u in uniques:
#         print(u)
#         if type(u) == float:
#             continue
#         levels_dict[u]=[[], 0, []]
#         rows = [i for i, x in enumerate(list(full_dataframe[c])) if x == u]
#         levels_dict[u][0]=c
#         for row in rows:
#             levels_dict[u][1]+=full_dataframe.loc[row,'total sequences']
#             levels_dict[u][2]+=full_dataframe.loc[row,'sequences'].strip("'[]").split("', '")

# print('making dataframe!')
# levels_frame=pd.DataFrame({'tax name':[], 'rank':[], 'total sequences':[], 'sequences':[]})

# for k in range(0,len(levels_dict.keys())):
#     print(k)
#     key=list(levels_dict.keys())[k]
#     levels_frame.loc[k, 'tax name']= key
#     levels_frame.loc[k, 'rank']= levels_dict[key][0]
#     levels_frame.loc[k, 'total sequences']= levels_dict[key][1]
#     levels_frame.loc[k, 'sequences']= str(levels_dict[key][2])
# levels_frame_no_seqs= levels_frame[['tax name', 'rank', 'total sequences']].copy()

# gen_frame=pd.DataFrame({'rank':[], 'tax names': [], 'total sequences':[]})

# gen_uniques=levels_frame_no_seqs['rank'].unique()
# gen_dict={}
# for u in gen_uniques:
# 	rows = [i for i, x in enumerate(list(levels_frame_no_seqs['rank'])) if x == u]
# 	gen_dict[u]=[[],0]
# 	for row in rows:
# 		gen_dict[u][0].append(levels_frame.loc[row,'tax name'])
# 		gen_dict[u][1]+=int(levels_frame.loc[row,'total sequences'])
# for k in range(0,len(gen_dict.keys())):
#     print(k)
#     key=list(gen_dict.keys())[k]
#     gen_frame.loc[k,'rank']=key
#     gen_frame.loc[k,'tax names']=str(gen_dict[key][0])
#     gen_frame.loc[k,'total sequences']=int(gen_dict[key][1])
     
        
# levels_frame.to_csv('/ifs/groups/rosenMRIGrp/jv545/DeepLearning/qiime_tutorial/jv545_work/Silva/ncbi_work/results/sequences_per_rank_and_name.csv', index=False)
# levels_frame_no_seqs.to_csv('/ifs/groups/rosenMRIGrp/jv545/DeepLearning/qiime_tutorial/jv545_work/Silva/ncbi_work/results/total-only_sequences_per_rank.csv', index=False)
# gen_frame.to_csv('/ifs/groups/rosenMRIGrp/jv545/DeepLearning/qiime_tutorial/jv545_work/Silva/ncbi_work/results/sequences_per_general_rank.csv', index=False)

# print('the following tax ids are in our file but not in the ncbi database: ' + str(weirds))
# print('These are the following extra taxa: '+ str(cats))
