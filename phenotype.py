'''
For creating each of the phenotype fils from the alltraits_allnormalized.csv 
file
'''

import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np
import csv
import statistics

import pandas_plink
from os.path import join
from pandas_plink import read_plink
from pandas_plink import get_data_folder

import scipy.stats as s
from scipy.stats import kruskal
from tqdm import tqdm

traits = pd.read_csv('/projects/ps-palmer/tsanches/gwaspipeline/gwas/allratsGRM/ALLTRAITS_ALLNORMALIZED.csv', low_memory = False)traits = pd.read_csv('/projects/ps-palmer/tsanches/gwaspipeline/gwas/allratsGRM/ALLTRAITS_ALLNORMALIZED.csv', low_memory = False)

traits.set_index('rfid', inplace = True)
traits = traits.loc[:, traits.columns.str.contains('regressedlr')]

traits.duplicated().sum()
traits = traits.reset_index().drop_duplicates(subset=['rfid']).set_index('rfid', drop = True)

for c in traits.columns:
    #FAM Id, RFID, TraitValue
    newdf = pd.DataFrame(traits[c])
    newdf = newdf.reset_index().dropna()
    newdf['rfid_dup'] = newdf.loc[:, 'rfid']
    newdf = newdf.loc[:,['rfid','rfid_dup',c]]
    newdf.rename(columns={"rfid": "FID", "rfid_dup": "IID",c: c}, inplace = True)
    newdf.to_csv(f'/projects/ps-palmer/samuckadam/code/plink_phenotypes/{c}.phen', sep='\t', index=False)