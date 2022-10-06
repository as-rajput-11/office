import glob
from itertools import count
import pandas as pd
import numpy as np



files = glob.glob('**/*.xlsx', recursive = True)
print("Found Excel Files :",files)
for file in files:
    print("Current open excel file :",file)
    df = pd.read_excel(file)
    print("Column names : ",df.columns.values)
    a = str(input('Enter delete column num: '))
  
    a = a.split(",")
    x = [eval(i) for i in a]
    df = df.drop(columns=df.columns[x])
    writer = pd.ExcelWriter(f'/home/bisag/glob/update/'+file)
 
    
    df.to_excel(writer,index= False)
    writer.save()
