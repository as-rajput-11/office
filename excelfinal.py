import glob
from itertools import count
import pandas as pd
import numpy as np
from termcolor import colored



files = glob.glob('**/*.xlsx', recursive = True)
print("Found Excel Files :",files)
for file in files:
    print("Current open excel file :",file)
    df = pd.read_excel(file)
    # print("Column names : ",df.columns.values)
    print("Columns names : ",[list((i, df.columns.values[i])) for i in range(len(df.columns.values))])
    a = str(input(colored('Enter Delete Column Num: ','red')))
  
    a = a.split(",")
    x = [eval(i) for i in a]
    df = df.drop(columns=df.columns[x])
    # print("Update columns : ",df.columns.values)
    print("Update Columns names : ",[list((i, df.columns.values[i])) for i in range(len(df.columns.values))])
    writer = pd.ExcelWriter(f'/home/bisag/glob/update/'+file)
 
    
    df.to_excel(writer,index= False)
    writer.save()






