#!/usr/bin/env python
# coding: utf-8

"""
CMIP6_errata_check.py
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
Contributors:       Kate Snow (kate.snow@anu.edu.au)
This code reads the synda database data for datasets located at NCI, and
compares it to the .txt files of datasets affected by errata in the notifications.
It then returns a list of all erroneous datasets that have been recored by the
errata notification and are located on the NCI filesystems. Action needs to be
taken for all such affected datasets. 
"""

import os
import glob
import gzip

def main():

    #Get the latest db backup from al33
    list_of_files = glob.glob('/g/data/oi10/admin/dtn/db/*')
    latest_file = sorted(list_of_files, key=os.path.getctime)[-2] #get second latest in case latest is still writing...

    #open the issue data txt files and read in the datasets
    with open('/g/data/oi10/admin/dtn/log/errata/201905/306c5df5-de28-9a5d-a9d3-46b41ad7a76f.txt','rb') as f:
        content_iss = f.readlines()
    content_iss = [x.strip() for x in content_iss] #remove all white-spaces
    content_iss = [x.decode() for x in content_iss] #decode all elements
    content_iss = [x for x in content_iss if x] #remove empty strings

    #open the db
    with gzip.open(latest_file) as f:
        content = f.readlines()
        content = [(x.decode()).strip() for x in content]

    #sort through sql entries to get info wanted (from dataset_id)
    for i in range(len(content)):
        paths = content[i]
        split = paths.split(',')

        #Get the indices for the dataset_functional_id from when the table is created 
        if "CREATE TABLE dataset " in split[0]:
            for i in range(len(split)):
                split[i]=split[i].strip()
            idx_data_id = split.index("dataset_functional_id TEXT")

        #load the datasets
        if "INSERT INTO \"dataset\"" in split[0]:
            dataset_id=split[idx_data_id].strip()
            for data in content_iss:
                if data in dataset_id:
                    print('This dataset on oi10 is affected ',dataset_id)

    return 

if __name__ =='__main__':
    main()
