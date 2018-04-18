import pandas as pd
import numpy as np
import os

DATA_DIR = '../data'

samples = pd.read_csv(os.path.join(DATA_DIR, 'samples.csv'))

NUM_SAMPLES = samples.shape[0]
PEOPLE = 3

#index = np.random.permutation(block.shape[0])[0:NUM_SAMPLES]
index = range(samples.shape[0])
for i in range(PEOPLE):
  step = int(NUM_SAMPLES/PEOPLE)
  sample = samples.iloc[index[0 + i*step : (i+1)* step], :]
  filename = 'sample_' + str(i) + '.csv'
  sample.to_csv(os.path.join(DATA_DIR, filename))

