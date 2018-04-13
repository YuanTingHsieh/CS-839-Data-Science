import pandas as pd
import numpy as np
import os

DATA_DIR = '../data'

samples = pd.read_csv(os.path.join(DATA_DIR, 'samples.csv'))
np.random.seed(7)

NUM_SAMPLES = samples.shape[0]
PEOPLE = 3

#index = np.random.permutation(block.shape[0])[0:NUM_SAMPLES]
index = range(samples.shape[0])
for i in range(PEOPLE):
  sample = samples.iloc[index[0 + i*NUM_SAMPLES/PEOPLE: (i+1)*NUM_SAMPLES/PEOPLE], :]
  filename = 'sample_' + str(i) + '.csv'
  sample.to_csv(os.path.join(DATA_DIR, filename))


