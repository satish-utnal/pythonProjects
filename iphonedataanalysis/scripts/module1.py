import pandas as pd

pd.options.display.max_columns = 5000
pd.set_option('display.max_columns', 5000)

df = pd.read_csv("../data/iphone.csv")
new_cols = []
[new_cols.append(col.replace(' ', '_')) for col in df.columns]
df.columns = new_cols
