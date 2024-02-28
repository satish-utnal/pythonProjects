# @Author Satish Utnal
"""
1 - The column names have spaces . rename the column names to have underscore '_' instead
of space (try to do in one go instead of specifying each column nam in rename method)

"""
import pandas as pd

pd.options.display.max_columns = 5000
pd.set_option('display.max_columns', 5000)
pd.set_option('display.max_rows', 5000)

df = pd.read_csv("../data/iphone.csv")
new_cols = []
[new_cols.append(col.replace(' ', '_')) for col in df.columns]
df.columns = new_cols

"""

2- start rating for some models is missing in the dataset.
fill those missing values with the average rating all the models.

"""
df_copy = df.copy()
avg = df['Star_Rating'].mean()
df['Star_Rating'].fillna(avg)

"""
3- Now instead of filling missing values with avg rating of full dataset , 
fill with avg rating based on RAM. example :  
if rating for a 2 gb phone is missing then take average of all other 2 gb phones rating and fill that value. 
"""

df = df_copy
avg = df[df['Ram'] != '2 GB']['Star_Rating'].mean()
df_2gb = df['Ram'] == '2 GB'
df.loc[df_2gb, 'Star_Rating'] = df.loc[df_2gb, 'Star_Rating'].fillna(avg)

print(df[['Ram','Star_Rating']])
print(df.info())
