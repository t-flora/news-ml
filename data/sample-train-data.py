import pandas as pd
import os
import glob
from datetime import datetime

timestamp = datetime.now().strftime("%d-%b-%H:%M")
filename = max(glob.iglob("./csvfiles/*.csv"), key = os.path.getmtime)
train_frac = 0.8
seed = 2022

df = pd.read_csv(filename)

sample = df.sample(frac = train_frac, replace = False, random_state = seed)
sample.to_csv(f"train-{timestamp}.csv")