import pandas as pd
import random
import pdb
import argparse


parser = argparse.ArgumentParser(description="Get numbers for ranks")
parser.add_argument('start', type=str, help="row in the seqs_for_each_[rank] file to start getting sequences from; each row corresponds with a label")
parser.add_argument('output', type=str, help="location of the output directory")
args = parser.parse_args()

#-------------------------------------start of variables and user inputs--------------------------------#

output=str(args.output)

#-----------use this if you are looking at one label per array job 
start=int(args.start)
end=start

#-------use the code below if you are trying to iterate through a section of rows per array job (for example, array job 0 would go through rows 0-9, while array job 1 goes through 10-19)
# row_group_size=10
# start=int(args.start) * row_group_size
# end=start + (row_group_size - 1)


# ranks=['phylum', 'class', 'order', 'family', 'genus', 'species']   <--- use if you are looping through all tax ranks; they're filled with lots of sequences though, so this would be very slow
ranks=['phylum']


#one of our datasets takes 10% of the sequences across all labels that have 10 or more sequences; you can change those items here though
percentage=0.1
threshhold=10
# print('yoo')

labels_divider=0.5     #what percentage of the labels are you considering for training
labels_seqs_divider=0.5    #in each chosen label, what percentage of their sequences would you actually use for training?
# percentage_number=1/percentage_number

#-----------Input files here! Make sure they match how your directories/files are formatted and that the paths are correct
Fasta_file='/ifs/groups/rosenMRIGrp/jv545/DeepLearning/qiime_tutorial/jv545_work/Silva/DNA_SILVA_138.1_SSURef_NR99_tax_silva.fasta'
Prefix_seqs_for_each='results/seqs_per_rank/seqs_for_each_'
Labels_chosen='results/chosen_'+str(labels_divider*100)+'/'+ranks[0]+'_chosen_half.txt'

#---------------------------End of variables and user_inputs------------------------------------------#

with open(Fasta_file) as f:
    all_seqs=f.read().splitlines()
all_seq_headers=[x for x in all_seqs if x.startswith('>')]
all_seq_shorts=[x.split(' ')[0] for x in all_seq_headers]

for r in ranks:
    chosen_headers_percentage=[]
    chosen_seqs_percentage=[]
    lis_percentage=[]
    test_headers_percentage=[]
    test_seqs_percentage=[]
    test_lis_percentage=[]

    chosen_headers_label_seqs=[]
    chosen_seqs_label_seqs=[]
    lis_label_seqs=[]
    test_headers_label_seqs=[]
    test_seqs_label_seqs=[]
    test_lis_label_seqs=[]

    weirds=[]

    # csv=pd.read_excel('results/sequences_per_rank.xlsx', r)
    csv=pd.read_csv(Prefix_seqs_for_each+r+'.csv')
    # csv=pd.read_csv('results/seqs_for_each_'+r+'.csv')

    # labels=list(csv.loc[start,(r+' label')])
    labels=csv.loc[start:end,(r+' label')].to_list()
    # good_labels=[csv.loc[x,(r+' label')] for x in range(0,len(csv.loc[:,(r+' label')])) if int(csv.loc[x, 'total sequences']) >= 2]
    # pdb.set_trace()
    with open(Labels_chosen) as f:
        good_label_seqs=f.read().splitlines()
    # headers_label_seqs=random.sample(good_label_seqs, int(0.5*len(good_labels)))
    for i in labels:
        # if i == 'Cryptococcus neoformans':
        #     print('yoo')
        # print(i)
        row=list(csv.loc[:,(r+' label')]).index(i)
        print(r + '--->' + i +'   ' + str(labels.index(i)/len(labels)))
        # print(type(csv.loc[row,(r+' label')]))
        # if int(csv.loc[row, 'total sequences']) < 10 or type(csv.loc[row,(r+' label')]) == float:
        #     continue
        # pdb.set_trace()
        headers=csv.loc[row, 'sequences'].replace('"','').replace("'",'').strip("'[]").split(", >")
        # l_headers=csv.loc[row, 'sequences']
        headers=[x.replace('\\','') for x in headers]
        # for x in headers:
        #     print(x)
        #     print('\n')
        # for x in headers:
        #     if '>' not in x:
        #         headers[headers.index(x)]='>'+x
        if len(headers)<threshhold and i not in good_label_seqs:   #NOTE: I made it so that if there's less than 10 sequences and the label is not one of the 50% chosen, the label gets skipped 
            continue

        if i in good_label_seqs:
            headers_label_seqs=random.sample(headers, int(labels_seqs_divider*len(headers)))
        else:
            headers_label_seqs=[]
        
        if len(headers) >=threshhold:
            headers_percentage=random.sample(headers, int(percentage*len(headers)))
        else:
            headers_percentage=[]
        # for x in headers_percentage:
        #     if '>' not in x:
        #         x='>' +x

        counter=0
        for h in headers:
            # if 'CP001969.3027330' not in h:
            #     continue
            if not h.startswith('>'):
                head='>'+h
            else:
                head=h
            print(str(headers.index(h)) + ' : ' + h, flush=True)
            seq=''
            head=head.replace('\\','')
            # if '>' not in h:
            #     h='>'+h
            # pdb.set_trace()
            try:
                short_index=all_seq_shorts.index(head.split(' ')[0])
            except:
                short_index=all_seq_shorts.index(head.split(' ')[0].replace('U', 'T'))
            full_header=all_seq_headers[short_index]
            try:
                try:
                    index=all_seqs.index(full_header)
                except:
                    index=all_seqs.index(full_header.replace('U','T'))
            except:
                weirds.append(h)
                continue
            rest=''.join(all_seqs[all_seqs.index(all_seqs[index])+1:all_seqs.index(all_seqs[index])+40]) #a section of the file starting from the header loc; I know that the next section starts less than 40 lines after the header loc
            rest_end=rest.find('>')

            if len(headers) >= threshhold:
                if h in headers_percentage:
                    chosen_headers_percentage.append(full_header)
                    chosen_seqs_percentage.append(rest[:rest_end])
                    lis_percentage.append(csv.loc[row, r+' label'])
                else:
                    test_headers_percentage.append(full_header)
                    test_seqs_percentage.append(rest[:rest_end])
                    test_lis_percentage.append(csv.loc[row, r+' label'])
            
            if h in headers_label_seqs:
                chosen_headers_label_seqs.append(full_header)
                chosen_seqs_label_seqs.append(rest[:rest_end])
                lis_label_seqs.append(csv.loc[row, r+' label'])
            else:
                test_headers_label_seqs.append(full_header)
                test_seqs_label_seqs.append(rest[:rest_end])
                test_lis_label_seqs.append(csv.loc[row, r+' label'])

            # counter+=1
            # for i in range(index+1,len(all_seqs)):
            #     if all_seqs[i].startswith('>'):
            #         end=i
            #         break
                    # pdb.set_trace()
            # seq=''.join(all_seqs[index+1:end]) >FN182235.1.1716
            # pdb.set_trace()
            # chosen_seqs.append(seq)
        # lis+=[csv.loc[row, r+' label']]*int((0.5*len(csv.loc[row, 'sequences'].strip("'[]").split("', '"))))
        # lis+=[csv.loc[row, r+' label']]*int(counter)
        # pdb.set_trace()
    # remaining_label_seqs=[x for x in good_label_seqs if x not in ]
    
    with open(output+'/training_'+str(labels_divider*100)+'-'+str(labels_seqs_divider*100)+'-'+r+'.txt', 'a') as f:
        for i in range(0,len(chosen_headers_label_seqs)):
            try:
                f.write(chosen_headers_label_seqs[i])
                f.write(' | ')
                f.write(lis_label_seqs[i])
                f.write('\n')
                # pdb.set_trace()
                f.write(chosen_seqs_label_seqs[i])
                f.write('\n')
            except:
                pdb.set_trace()
    with open(output+'/testing_'+str(labels_divider*100)+'-'+str(labels_seqs_divider*100)+'-'+r+'.txt', 'a') as f:
        for i in range(0,len(test_headers_label_seqs)):
            try:
                f.write(test_headers_label_seqs[i])
                f.write(' | ')
                f.write(test_lis_label_seqs[i])
                f.write('\n')
                # pdb.set_trace()
                f.write(test_seqs_label_seqs[i])
                f.write('\n')
            except:
                pdb.set_trace()
    with open(output+'/training_'+str(percentage*100)+'-percent-'+r+'.txt', 'a') as f:
        for i in range(0,len(chosen_headers_percentage)):
            try:
                f.write(chosen_headers_percentage[i])
                f.write(' | ')
                f.write(lis_percentage[i])
                f.write('\n')
                # pdb.set_trace()
                f.write(chosen_seqs_percentage[i])
                f.write('\n')
            except:
                pdb.set_trace()
    with open(output+'/testing_'+str(percentage*100)+'-percent-'+r+'.txt', 'a') as f:
        for i in range(0,len(test_headers_percentage)):
            try:
                f.write(test_headers_percentage[i])
                f.write(' | ')
                f.write(test_lis_percentage[i])
                f.write('\n')
                # pdb.set_trace()
                f.write(test_seqs_percentage[i])
                f.write('\n')
            except:
                pdb.set_trace()
    
    if weirds != []:
        with open(output+'/'+r+'-still_missing.txt', 'a') as f:
            for i in weirds:
                f.write(i)
                f.write('\n')