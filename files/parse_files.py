import pandas as pd
import numpy as np

def parse_file(filename):
    df = pd.read_csv(filename)
    df = df.replace(np.nan, None)
    entries = df.to_dict('records')
    
    return entries