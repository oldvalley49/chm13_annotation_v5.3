import pandas as pd
import os
for file in os.listdir('changes_paired/'):
    fp = 'changes_paired/' + file
    df = pd.read_csv(fp, index_col = 0)
    df['start_add'] += 2
    #df['start_remove'] += 2
    df.to_csv(fp)

