import pandas as pd
import os

output_dir='results'
output_prefix='fixed_all_tax_ids'
scratch_dir='/scratch/jv545/ncbi'
#----------------End of Inputs---------------

numbers_dict={}
os.chdir(scratch_dir)
counter=0
for file in os.listdir():  #loop through each file and make a dictionary for the sequences for each taxID
    # print(counter)
    table=pd.read_csv(file)
    for i in range(0,len(table.iloc[:,0])):
        print(str(counter) + '-->' + str(i/len(table.iloc[:,0])))
        if int(table.iloc[i,0]) not in numbers_dict.keys():
            numbers_dict[int(table.iloc[i,0])]=[0, []]
        numbers_dict[int(table.iloc[i,0])][1]+=(table.iloc[i,1].strip("'[]").split("', '"))   #add the list of sequences to the taxID; if there already is a list, the new sequences are added to it
    counter+=1
for i in numbers_dict.keys():
    numbers_dict[i][0]=len(str(numbers_dict[i][1]).replace('"','').replace("'",'').strip("'[]").split(", >"))   #count the number of sequences for each taxID
df=pd.DataFrame({'taxID':[], 'total sequences':[], 'sequences': []})
max=0

#turn the dictionary into a dataframe
for i in range(0,len(numbers_dict.keys())):
    print(i/len(numbers_dict.keys()))
    key=int(list(numbers_dict.keys())[i])
    df.loc[i,'taxID']=key
    df.loc[i, 'total sequences']=int(numbers_dict[key][0])
    df.at[i, 'sequences']=str(numbers_dict[key][1]).replace("'","")
    # if '\\' in df.loc[i, 'sequences']:
    #     print('yooo')
df=df.sort_values(by='total sequences', ascending=False)
df = df.replace(to_replace= r'\\', value= '', regex=True)
print('--------------')
print('species')
print('The TaxIDs with the top 10 most sequences are: ' + str(list(df.iloc[0:10,0])))
print('They have the following number of sequences' + str(list(df.iloc[0:10,1])))
df.to_csv(output_dir+'/'+output_prefix+'.csv', index=None)
