import psycopg2
import pandas as pd


conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="localhost", port="5432")

dataframe1 = pd.read_excel('d.xlsx')

# dataframe2 =dataframe1.columns
print(dataframe1)
for i ,r in dataframe1.iterrows():
    cur = conn.cursor()
    cur.execute("insert into ditance_station values('" + r['f_station'] + "','" + r['d_station'] + "'," + str(r['distance']) +')')
    conn.commit()
    cur.close()
    print(r['f_station'],r['d_station'],r['distance'])
    

cur = conn.cursor()
