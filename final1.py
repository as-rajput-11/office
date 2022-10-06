 
import glob
from itertools import count
import uuid
import pandas as pd
import numpy as np
from uuid import uuid4
files = glob.glob('**/*.xlsx', recursive = True)
print("Found Excel Files :",files)

for file in files:
    c = 1
    print("Current open excel file :",file)
    df = pd.read_excel(file)
    print("Column names : ",df.columns.values)
    x = []
    while c == 1:
        
        a = int(input('Enter delete column num: '))
        x.append(a)
        print('More delete column then press C and for next file press D')
        moreDelete = str(input())
        if moreDelete == 'c' or moreDelete == 'C':
            pass
        elif moreDelete == 'd' or moreDelete == 'D':
            c = 2 
        else:
            break
    df = df.drop(columns=df.columns[x])
    print(df)
    # writer = pd.ExcelWriter(f'/home/bisag/glob/update/{uuid.uuid4()}.xlsx')
    writer = pd.ExcelWriter(f'/home/bisag/glob/update/'+file)
  
 
    df.to_excel(writer)
    writer.save()
 
