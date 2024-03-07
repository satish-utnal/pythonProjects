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

"""
4- create a new column in the dataframe "Discount_Percentage" based on MRP and sale value

"""

df['Discount_Percentage'] = round((((df["Mrp"] - df["Sale_Price"]) / df["Mrp"]) * 100), 2)

"""
5- which model has highest percent discount ?
"""
df_high_discount = df.sort_values('Discount_Percentage', ascending=False).head(1)

print(df_high_discount["Product_Name"])

"""
6- find total no of models  each space configuration (128 GB , 64 GB etc)

"""

df['Space'] = df['Product_Name'].apply(lambda x: x[x.find(',') + 1:-1])
df_model_groups = df.groupby('Space')['Product_Name'].count().reset_index()
df_model_groups.rename(columns={'Product_Name': 'Total_Models'}, inplace=True)
print(df_model_groups)


"""

7- find total number of models for each color 

"""

df["Color"] = df['Product_Name'].apply(lambda x: x[x.find('(') + 1:x.find(',')])
df_color_group = df.groupby(["Color"])['Product_Name'].count().reset_index()
df_color_group.rename(columns={'Product_Name': 'Total_Models'}, inplace=True)
print(df_color_group)


"""
8- find total number of models by iphone version : eg
iphone 8:  9
iphone XR : 5

so on..
"""
df['Version'] = df['Product_Name'].apply(lambda x: x[: x.find('(')])
df_version_group = df.groupby('Version')['Product_Name'].count().reset_index()
df_version_group.rename(columns={'Product_Name': 'Total_Models'})
print(df_version_group)

"""

9- list top 5 models having highest no of reviews 

"""
print(df[["Product_Name", "Number_Of_Reviews"]].sort_values('Number_Of_Reviews', ascending=False).head(5))

"""
10 - what is the price difference between highest price and lowest price iphone (based on mrp)

"""
price_diff = max(df['Mrp']) - min(df['Mrp'])
print(f" {price_diff} ")


"""
11 - find total no of reviews for iphone 11 and iphone 12 category . Output should have only 2 rows (for 11 and 12).

"""
condition = df['Product_Name'].str.contains('iPhone 11')
df.loc[condition, 'category'] = 'APPLE iPhone 11'
condition = df['Product_Name'].str.contains('iPhone 12')
df.loc[condition, 'category'] = 'APPLE iPhone 12'
df_category_11_12 = df.groupby('category')["Number_Of_Reviews"].sum().reset_index()
print(df_category_11_12)


"""
 12- which iphone has 3rd highest MRP
"""
df_3rd_highest = df.sort_values('Mrp', ascending=False).reset_index()
df_3rd_highest['rnk'] = df_3rd_highest['Mrp'].rank(method='dense', ascending=False)

print(df_3rd_highest[df_3rd_highest['rnk'] == 3])
"""
13- what is the average mrp of iphones which costs above 100,000
"""
df_average = df[df['Mrp'] > 10000]
print(round(df_average['Mrp'].mean(),2))
"""
14- which iphone with 128 GB space has highest ratings to review ratio
"""

print(df[df['Space'].str.contains('128 GB')].sort_values('Number_Of_Ratings', ascending=False).head(1))



