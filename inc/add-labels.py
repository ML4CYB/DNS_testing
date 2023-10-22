# add-labels.py
# Author: Chris Wieringa <chris@wieringafamily.com>
# Purpose: quickly label a DoHlyzer CSV file with known DoH servers

import pandas as pd, numpy as np

# Variable definitions
filename = input("Please enter the filename to read: ")
filenameout = input("Please enter the filename to output to: ")

# Main Program
# Open the CSV and read it in via Pandas
data = pd.read_csv(filename)
data=data.drop(['DoH'],axis=1)

labels = []

for index,row in data.iterrows():
    # check for DoH traffic
    dohservers = ['104.16.248.249','102.16.249.249','8.8.8.8','8.8.4.4']
    if row['SourceIP'] in dohservers or row['DestinationIP'] in dohservers: 
        labels.append('DoH')
    else:
        labels.append('NonDoH')

data['Label'] = labels
data.to_csv(filenameout,index=False)