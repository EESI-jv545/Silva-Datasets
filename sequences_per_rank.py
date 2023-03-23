import pandas as pd
import pdb
# import math
# from ete import NCBITaxa
# import openpyxl

# ncbi = NCBITaxa()

ids_w_taxas_file='results/fixed_all_ids_w_taxonomy.csv'
out_dir='results/seqs_per_rank/'
output_prefix='seqs_for_each_'   #make sure to change this to something like "sequences_per_All_Ranks" if you are making csv files for each rank
#---------------End of Inputs----------------------

full_dataframe=pd.read_csv(ids_w_taxas_file)
excludes=[]
# ----
######This section creates an summary excel file with tabs for each rank; however, the list of sequences per rank is cut off when you 
##########          write it to an excel file, so if you don't need the summary file, you can leave this out
levels_dict={}
for c in full_dataframe.columns[2:10]:  #start by getting the sequences per rank label in a dictionary
    uniques=full_dataframe[c].unique()
    for u in uniques:
        print(c + ' ---> ' + str(list(uniques).index(u)/len(uniques)) + '  ' + str(u))
        if type(u) == float:
            continue
        levels_dict[u]=[[], 0, []]
        rows = [i for i, x in enumerate(list(full_dataframe[c])) if x == u]  #look for all the rows with that rank label
        levels_dict[u][0]=c
        for row in rows:
            # if full_dataframe.loc[row,'superkingdom'] in ['Eukaryota', 'Viruses']:     #this part's useful if you only want prokaryotes
                # excludes.append(full_dataframe.loc[row,'taxID'])
                # continue
            levels_dict[u][2]+=full_dataframe.loc[row,'sequences'].strip("'[]").split("', '")   #add the list of sequences to that rank label 
        # if u == 'Viruses':
        #     pdb.set_trace()

for key in levels_dict.keys():
    print(key)
    if levels_dict[key][2] ==[]:
        levels_dict[key][1] = 0
        continue
    levels_dict[key][1]=len(str(levels_dict[key][2]).replace('"','').replace("'",'').strip("'[]").split(", >"))   #count the number of sequences for that rank label

print('making dataframe!')
levels_frame=pd.DataFrame({'tax name':[], 'rank':[], 'total sequences':[], 'sequences':[]})
# levels_frame=pd.DataFrame({'tax name':[], 'rank':[], 'total sequences':[]})

counter=0
for k in range(0,len(levels_dict.keys())):   #turn the dictionary into a dataframe
    print(k)
    if levels_dict[list(levels_dict.keys())[k]][1] == 0:
        continue
    key=list(levels_dict.keys())[k]
    levels_frame.loc[counter, 'tax name']= key
    levels_frame.loc[counter, 'rank']= levels_dict[key][0]
    levels_frame.loc[counter, 'total sequences']= levels_dict[key][1]
    counter+=1

#now use that dataframe to get the number of sequences per rank
gen_frame=pd.DataFrame({'rank':[], 'total labels':[], 'labels': [], 'total sequences':[]})

gen_uniques=levels_frame['rank'].unique()
gen_dict={}
for u in gen_uniques:
	rows = [i for i, x in enumerate(list(levels_frame['rank'])) if x == u]
	gen_dict[u]=[[],0]
	for row in rows:
		gen_dict[u][0].append(levels_frame.loc[row,'tax name'])
		gen_dict[u][1]+=int(levels_frame.loc[row,'total sequences'])
for k in range(0,len(gen_dict.keys())):
    print(k)
    key=list(gen_dict.keys())[k]
    gen_frame.loc[k,'rank']=key
    gen_frame.loc[k,'total labels']=len(gen_dict[key][0])
    gen_frame.loc[k,'labels']=str(gen_dict[key][0])
    gen_frame.loc[k,'total sequences']=int(gen_dict[key][1])
     
gen_frame=gen_frame.sort_values(by='total sequences', ascending=False)
# ## levels_frame.to_csv('/ifs/groups/rosenMRIGrp/jv545/DeepLearning/qiime_tutorial/jv545_work/Silva/ncbi_work/sequences_per_rank_and_name.csv', index=False)
# ## levels_frame_no_seqs.to_csv('/ifs/groups/rosenMRIGrp/jv545/DeepLearning/qiime_tutorial/jv545_work/Silva/ncbi_work/total-only_sequences_per_rank.csv', index=False)
with pd.ExcelWriter(out_dir+"/"+output_prefix+".xlsx") as writer:
    gen_frame.to_excel(writer, sheet_name="all ranks", index=False)

# -----
# file=pd.read_csv(r'results/Psudeomonadota_full_info.csv')
# file.to_excel (r'results/Psudeomonadota_full_info.xlsx', index = None, header=True)
# rows = [i for i, x in enumerate(list(full_dataframe['phylum'])) if x == 'Pseudomonadota']

levs=['superkingdom', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
# levs=['phylum', 'class', 'order', 'family', 'genus']

counter=0
for lev in levs:   #now for each rank, get the number of sequences per label and make a CSV file and Excel tab
    # if lev!='family':
    #     continue
    # elif lev == 'superkingdom':
    #     continue
    # print(lev)
    levels_dict={}
    labels=[]
    uniques = full_dataframe[lev].unique()
    counter=0
    for u in uniques:
        print(lev + '--->' + str(u))
        rows=[i for i, x in enumerate(list(full_dataframe[lev])) if x == u]
        key=[]
        for row in rows:
            if type(full_dataframe.loc[row,lev]) == float:
                continue
            # if full_dataframe.loc[row,'superkingdom'] in ['Eukaryota', 'Viruses']:
            #     continue
            key=full_dataframe.loc[row,lev]
            # if row == 9:
            #     print('yooo')
            # if full_dataframe.loc[row,lev] == 'Bacteria' and lev!= 'superkingdom':
            #     print('yooo')
            if full_dataframe.loc[row,lev] not in labels:
                labels.append(full_dataframe.loc[row,lev])
                levels_dict[full_dataframe.loc[row,lev]]=[0, []]
            # if '\\' in full_dataframe.loc[row,'sequences']:
            #     print('yooo')
            # levels_dict[full_dataframe.loc[row,lev]][0]+=full_dataframe.loc[row,'total sequences']
            levels_dict[full_dataframe.loc[row,lev]][1]+=full_dataframe.loc[row,'sequences'].strip("'[]").split("', '")
            # if '\\' in levels_dict[full_dataframe.loc[row,lev]][1]:
            #     print('yooo')
        if key != []:
            levels_dict[key][0]=len(str(levels_dict[key][1]).replace('"','').replace("'",'').strip("'[]").split(", >"))
        counter+=1

    frame=pd.DataFrame({lev+' label':[], 'total sequences':[], 'sequences':[]})
    for k in range(0,len(levels_dict.keys())):
        key=list(levels_dict.keys())[k]
        frame.loc[k, lev+' label']=key
        frame.loc[k, 'total sequences']=levels_dict[key][0]
        frame.loc[k, 'sequences']=str(levels_dict[key][1])
        # frame.loc[k, 'sequences']=str(levels_dict[key][1]).replace("'",'').replace('"','').strip("[]'").split(', >')
        # frame.loc[k, 'total sequences']=len(frame.loc[k, 'sequences'])
    # pdb.set_trace()
    frame=frame.sort_values(by= 'total sequences', ascending=False)
    frame=frame.replace("'", "")
    # print('yooo')

    frame.to_csv(out_dir+'/'+output_prefix+lev+'.csv', index=None)

    #---Use the code below if you are making the summary file. This section makes the individual tabs
    # with pd.ExcelWriter(out_dir+"/"+output_prefix+".xlsx", mode="a", engine="openpyxl") as writer:
    #     frame.to_excel(writer, sheet_name=lev, index=False)
