import pandas as pd
import os


# inform if some error occurred while reading
try:
    df = pd.read_csv("data.csv", sep=",", header=None)
except Exception as e:
    print("SIGMA BASED CSV CHECKER: exception was raised while reading data.csv:", e)
    exit(1)

# imho: service should have user interface
if 'CSV_VERBOSE' in os.environ:
    print('===== SIGMA BASED CSV CHECKER =====\n    Do values sum to 10:', end=' ')

# imho: all non-numeric values should be ignored
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

print(df.values.sum() == 10)

if 'CSV_VERBOSE' in os.environ:
    print('===================================')
