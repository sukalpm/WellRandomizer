#!/usr/bin/env python
# coding: utf-8

# In[138]:


#Well Randomizer for Echo platform
#Changes required from user - file paths for input file, output mapping file, and output randomized file
import pandas as pd
import numpy as np
import sys
import argparse
import csv
import os
pd.set_option('display.min_rows', 100)
parser = argparse.ArgumentParser(description='Well Randomizer v0.1')
parser.add_argument("-i", required = True, type = str, help="Input file")
parser.add_argument("-m", required = True, type = str, help="Output mapping file")
parser.add_argument("-o", required = True, type = str, help="Output randomized file")
args = parser.parse_args()
file = pd.read_csv(args.i, sep = ",").dropna().reset_index(drop = True)
#print(args)


# In[107]:


file['dest_bc/well'] = file['Destination Barcode'] + ":" + file['Destination Well']


# In[108]:


file['source_bc/well'] = file['Source Barcode'] + ":" + file['Source Well']


# In[109]:


pv = pd.pivot_table(file, index = 'dest_bc/well', values = ['Volume'], columns = ['source_bc/well'])


# In[110]:


df = pd.DataFrame(pv.to_records(), index = pv.index)
cols = [df.columns[0]]
for col in df.columns[1:]:
    cols.append(eval(col)[1])
df.columns = cols
df['dest_bc/well'] = np.random.permutation(df['dest_bc/well'])
df['old_mapping'] = df.index
df.index = df['dest_bc/well']
df2 = df.drop(['old_mapping', 'dest_bc/well'], axis = 1)


# In[111]:


rand_df = pd.DataFrame(columns = ['Source Barcode', 'Source Well', 'Destination Barcode', 'Destination Well', 'Volume'])
for row in df2.iterrows():
    for val in row[1].dropna().keys():
        rand_df = rand_df.append({'Source Barcode' : val.split(":")[0], 
                                  'Source Well' : val.split(":")[1], 
                                  'Destination Barcode' : row[0].split(":")[0], 
                                  'Destination Well' : row[0].split(":")[1], 
                                  'Volume' : row[1][val]}, 
                                ignore_index = True)


# In[112]:


df[['Destination Barcode', 'Destination Well']] = df['dest_bc/well'].str.split(":", expand = True)
df[['old_mapping_bc', 'old_mapping_well']] = df['old_mapping'].str.split(":", expand = True)
df[['Destination Well', 'old_mapping_bc', 'old_mapping_well']].to_csv(args.m, index = False)
rand_df.to_csv("tmp.csv", index = False)


# In[ ]:


with open("tmp.csv", 'r') as in_file:
    read = csv.reader(in_file, delimiter=',')
    with open(args.o, 'wt') as out_file:
        writer=csv.writer(out_file, delimiter=',')
        for row in read:
            writer.writerow(row)
            writer.writerow([])
os.remove("tmp.csv")

