import pandas as pd
import numpy as np
import os

DATA_DIR = '../data'
NUM_SAMPLES = 510
PEOPLE = 3

block = pd.read_csv(os.path.join(DATA_DIR, 'block.csv'))
np.random.seed(7)

index = np.random.permutation(block.shape[0])[0:NUM_SAMPLES]
for i in range(PEOPLE):
  sample = block.iloc[index[0 + i*NUM_SAMPLES/PEOPLE: (i+1)*NUM_SAMPLES/PEOPLE], :]
  filename = 'sample_' + str(i) + '.csv'
  sample.to_csv(os.path.join(DATA_DIR, filename))


