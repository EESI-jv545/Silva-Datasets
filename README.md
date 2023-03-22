# Silva-Datasets
**Github Repository to create Tax-Labeled Datasets from 16s Silva Sequences for multiple Tax Ranks**

**by James Virtucio** (jv545@drexel.edu)

---
Welcome! This is the workflow to get sequences for the SILVA Dataset. We start with a SILVA Fasta and NCBI Tax mapping file, and after assigning taxIDs and organizing sequences by taxononmy, we create two datasets, each with their own conditions:

-**Dataset 1:** We look at all of the sequences with 10 or more sequences and take 10% for training. The rest are used for testing

-**Dataset 2:** We take 50% of all labels that have 2 or more sequence, and 50% of the sequences in each label will be used for training. The rest (even sequences from unchosen labels) are used for testing

There is a Training and Testing File for each dataset, and both datasets are made from ranks going from phylum to genus (and optionally species)

---
To start this, you'll need the following input files<br>
<br>
    - **SILVA Fasta file with 16s sequences and headers**
        (sample name: [SILVA_138.1_SSURef_NR99_tax_silva.fasta](https://www.arb-silva.de/fileadmin/silva_databases/release_138_1/Exports/SILVA_138.1_SSURef_NR99_tax_silva.fasta.gz))<br>
    - **NCBI taxonomy mapping file to map SILVA sequences to NCBI taxids**
        (sample name: [tax_ncbi_ssu_ref_138.1.txt](https://www.arb-silva.de/fileadmin/silva_databases/release_138_1/Exports/taxonomy/ncbi/tax_ncbi_ssu_ref_138.1.txt.gz))<br>
    - You can also find the directory with the [16s sequences here](https://www.arb-silva.de/no_cache/download/archive/release_138_1/Exports/) and the directory for the [tax mapping files here](https://www.arb-silva.de/no_cache/download/archive/release_138_1/Exports/taxonomy/ncbi/)

Additionally, you'll also need to set up a python virtual environment. The packages that I use in my environent are:<br>
<br>
    - ete3<br>
    - numpy<br>
    - pip<br>
    - pandas<br>
    - python-dateutil<br>
    - pytz<br>
    - setup-tools<br>
    - et-xmlfile<br>
    - six<br>
    

---
If you are in a rush, you can just refer to the following workflow. Make sure you create output directories for your Slurm ".out"/".err" docs, as well as folders for all of your results; all of the programs in this Github Repository also have inputs that you can change to match your directory paths:

    mkdir /scratch/[USER ID]/ncbi/          <-- This makes the scratch directory that multi_ranks.sh writes to
    
    
    sbatch multi_ranks.sh                   <-- This gets the taxids per sequence by going through each rank of the sequence and trying to find it in the tax file; calls find_ranks.py
    
    python compile_ranks.py                 <-- This compiles all of the results from multi_ranks together; we iterate through alot of sequences, so I made the previous program work in groups
    
    python analyze_phyla.py                 <-- **[You need to activate the python-env beforehand]**   This gets the full taxonomic lineage per tax id, and creates a table for the sequences that have these lineages
    
    python sequences_per_rank.py            <-- This looks at the labels for each rank and sees which sequences have these labels
    
    python choose_50.py                     <-- This chooses 50% of the labels found in each rank; this will be used for one of our datasets later
    
    sbatch general-multi_make_datasets.sh   <-- This makes the datasets; you'll need to specify the tax rank, whether you want the program to loop through several rows, and a threshhold for the percentage of sequences to include
    
    ./all_ranks_debugger.sh                 <-- This checks through all of the datasets made for each rank makes sure we have the right number of sequences; calls datasets_debugger.py
    
