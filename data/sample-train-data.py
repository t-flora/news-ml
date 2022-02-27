import pandas as pd
import os
import glob
from datetime import datetime

timestamp = datetime.now().strftime("%d-%b-%H:%M")
cwd = os.getcwd()

filename = max(glob.iglob(f"{cwd}/csvfiles/*.csv"), key = os.path.getmtime)
train_frac = 0.8
seed = 2022

df = pd.read_csv(filename)

sample = df.sample(frac = train_frac, replace = False, random_state = seed)
sample.to_csv(f"{cwd}/xlsxfiles/train-{timestamp}.csv")