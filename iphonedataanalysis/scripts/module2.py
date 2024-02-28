


import module1 as m1

avg = m1.df['Star_Rating'].mean()

m1.df['Star_Rating'].fillna(avg)
