import pandas as pd
import random

ranks=['phylum', 'class', 'order', 'family', 'genus']
prefix=''
output='results'

labels_divider=0.5   #change this variable to change the percentage of labels to consider for testing

for r in ranks:

    csv=pd.read_csv(output+'/seqs_per_rank/'+prefix+'seqs_for_each_'+r+'.csv')

    labels=list(csv.loc[:,(r+' label')])
    good_labels=[csv.loc[x,(r+' label')] for x in range(0,len(csv.loc[:,(r+' label')])) if int(csv.loc[x, 'total sequences']) >= 2]   #choose 50% of the labels with 2 or more sequences; change this variable as needed
    # pdb.set_trace()
    chosen_labels=random.sample(good_labels, int(labels_divider*len(good_labels)))

    with open(output+'/chosen_'+str(labels_divider*100)+'/'+prefix+r+'_chosen_half.txt', 'w') as f:
        for i in chosen_labels:
            f.write(i)
            f.write('\n')
