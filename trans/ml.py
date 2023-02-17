import pandas as pd
import numpy as np
import plotly.express as px
df = pd.read_excel('CSV4.xlsx')
df.head(2)
df.isna().sum()

df['Materially Not Ready Days'].isna().sum()
fig = px.histogram(df, x='Materially Not Ready Days')
fig.show()
fig = px.box(df, x='Materially Not Ready Days')
fig.show()
df.rename(columns = {'Materially Not Ready Days':'Materially_Not_Ready_Days'}, inplace = True)
df.Materially_Not_Ready_Days.fillna(df.Materially_Not_Ready_Days.median(),inplace=True)

df.head(2)
df.isna().sum()
df['Days In Dry Docking'].isna().sum()
fig = px.histogram(df, x='Days In Dry Docking')
fig.show()
df['Days In Dry Docking'].isna().sum()
fig = px.box(df, x='Days In Dry Docking')
fig.show()
df.rename(columns = {'Days In Dry Docking':'Days_In_Dry_Docking'}, inplace = True)
df.Days_In_Dry_Docking.fillna(df.Days_In_Dry_Docking.median(),inplace=True)
df['Days_In_Dry_Docking'].isnull().values.any()
# print(df['Days_In_Dry_Docking'])
df.to_excel('del.xlsx')
df.isnull().sum()
df.rename(columns = {'ENGINEERING':'Opp_Def_ENGINEERING'}, inplace = True)
df.rename(columns = {'ELECTRICAL':'Opp_Def_ELECTRICAL'}, inplace = True)
df.rename(columns = {'HULL':'Opp_Def_HULL'}, inplace = True)
# df.isnull().sum()
df['Operational Exercise Days'].isna().sum()
fig = px.box(df, x='Operational Exercise Days')
fig.show()
df.rename(columns = {'Operational Exercise Days':'Operational_Exercise_Days'}, inplace = True)
df.Operational_Exercise_Days.fillna(df.Operational_Exercise_Days.median(),inplace=True)
df['Operational_Exercise_Days'].isnull().values.any()
df['Equipment Count'].isna().sum()
fig = px.box(df, x='Equipment Count')
fig.show()
df['Equipment Count'].isna().sum()
fig = px.histogram(df, x='Equipment Count')
fig.show()
df.rename(columns = {'Equipment Count':'Equipment_Count'}, inplace = True)
df.Equipment_Count.fillna(df.Equipment_Count.median(),inplace=True)
df['Equipment_Count'].isnull().values.any()
df['Opp_Def_ENGINEERING'].isna().sum()
fig = px.box(df, x='Opp_Def_ENGINEERING')
fig.show()
df['Opp_Def_ENGINEERING'].isna().sum()
fig = px.histogram(df, x='Opp_Def_ENGINEERING')
fig.show()
df.Opp_Def_ENGINEERING.fillna(df.Opp_Def_ENGINEERING.median(),inplace=True)
df.isnull().sum()
df['Total_Days'] = df['DecommissionDate'].sub(df['CommissionDate'], axis=0)
df.head(2)
# df.drop(["Difference"],axis=1)
df.isnull().sum().sort_values(ascending=0)
# list(df.columns)
df[['ShipName','Ship ID','ShipCode','CommissionDate','DecommissionDate','Ship Class','CommandRef',
 'Materially Ready Days',
 'Operational_Exercise_Days',
 'Distance Run in NM',
 'Ship Running Hours',
 'No Of Darts Raised',
 'Materially_Not_Ready_Days',
 'Days_In_Dry_Docking',
 'Equipment_Count',
 
 'Dart_ENGINEERING',
 'Dart_ELECTRICAL',
 'Dart_HULL',
 'Opp_Def_ENGINEERING',
 'Total_Days']]

missing_vnl=['ShipName','Ship ID','ShipCode','CommissionDate','DecommissionDate','Ship Class','CommandRef',
 'Materially Ready Days',
 'Operational_Exercise_Days',
 'Distance Run in NM',
 'Ship Running Hours',
 'No Of Darts Raised',
 'Materially_Not_Ready_Days',
 'Days_In_Dry_Docking',
 'Equipment_Count',
 
 'Dart_ENGINEERING',
 'Dart_ELECTRICAL',
 'Dart_HULL',
 'Opp_Def_ENGINEERING',
 'Total_Days']

df.to_excel('del1.xlsx',columns=missing_vnl)
# list(df.columns)
# df.isnull().sum().sort_values(ascending=0)
# df[['No. of MR Days','No. Of NR Days','No. Of AMP Days','Opp_Def_HULL','Days A Ship Went For SR','Days Went For Special Duty','Opp_Def_ELECTRICAL','Days A Ship Went For Refit']]
missing_vn =['ShipCode','No. of MR Days','No. Of NR Days','No. Of AMP Days','Opp_Def_HULL','Days A Ship Went For SR','Days Went For Special Duty','Opp_Def_ELECTRICAL','Days A Ship Went For Refit']
df.to_excel('del2.xlsx',columns = missing_vn)
vnl=pd.read_excel("del1.xlsx")
vnl.isnull().sum()

vn=pd.read_excel("del2.xlsx")
vn.isnull().sum()

dfnew = pd.read_excel('del1.xlsx')
dfnew1 = pd.read_excel('del2.xlsx')

# print(dfnew,dfnew1)
one = dfnew1.columns
data = one[9]
data1 = dfnew1[data]

con = pd.concat([dfnew, data1.reindex(dfnew.index)], axis=1)
# print(con)

con.to_csv('concated.csv')


# df3.tail(2)


x =con[['Ship ID',
 'Materially Ready Days',
 'Operational_Exercise_Days',
 'Distance Run in NM',
 'Ship Running Hours',
 'No Of Darts Raised',
 'Materially_Not_Ready_Days',
 'Days_In_Dry_Docking',
 'Equipment_Count',
 
 'Dart_ENGINEERING',
 'Dart_ELECTRICAL',
 'Dart_HULL',
 'Opp_Def_ENGINEERING',
 'Total_Days']]

y = con[['Days A Ship Went For Refit']]


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics


x_train, x_test, y_train, y_test= train_test_split(x, y, test_size= 0.3, random_state=100)  


mlr= LinearRegression()  
mlr.fit(x_train, y_train)  
