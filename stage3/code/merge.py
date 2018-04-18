import pandas as pd
import numpy as np
import os

DATA_DIR = '../data'

PEOPLE = 3

samples = []
for i in range(PEOPLE):
  filename = 'sample_' + str(i) + '.csv'
  sample = pd.read_csv(os.path.join(DATA_DIR, filename))
  samples.append(sample)

data = pd.concat(samples)
data.drop('Unnamed: 0', axis=1, inplace=True)
data.to_csv(os.path.join(DATA_DIR, 'new_label_data.csv'))
