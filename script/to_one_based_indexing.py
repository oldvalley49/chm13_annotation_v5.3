import pandas as pd
import os
for file in os.listdir('changes/'):
    fp = 'changes/' + file
    df = pd.read_csv(fp, index_col = 0)
    df['start'] += 1
    df.to_csv(fp)

