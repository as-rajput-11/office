import glob
from itertools import count
import uuid
import pandas as pd
import numpy as np
from uuid import uuid4


files = glob.glob('**/*.xlsx', recursive = True)
print("filesh",files)
for file in files:
    print(file)
    df = pd.read_excel(file)
    print(df.columns.values)
    x = int(input())
    print(x)
    # x = x.split(",")
    df = df.drop(columns=df.columns[x])
    writer = pd.ExcelWriter(f'{uuid.uuid4()}.xlsx')
   

    df.to_excel(writer)
    writer.save()
 



