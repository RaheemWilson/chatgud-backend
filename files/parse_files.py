import pandas as pd

def parse_file(filename):
    df = pd.read_csv(filename)
    entries = df.to_dict('records')
    
    return entries