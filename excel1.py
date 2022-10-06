import glob
from itertools import count
import uuid
import pandas as pd
import numpy as np
from uuid import uuid4
files = glob.glob('**/*.xlsx', recursive = True)
print("filesh",files)

for file in files:
    c = 1
    print(file)
    df = pd.read_excel(file)
    print(df.columns.values)
    x = []
    while c == 1:
        print('enter columan :')
        a = int(input())
        x.append(a)
        print('more delete columan then press C and for net file press D')
        moreDelete = str(input())import glob
from itertools import count
import uuid
import pandas as pd
import numpy as np
from uuid import uuid4
files = glob.glob('**/*.xlsx', recursive = True)
print("filesh",files)

for file in files:
    c = 1
    print(file)
    df = pd.read_excel(file)
    print(df.columns.values)
    x = []
    while c == 1:
        print('enter columan :')
        a = int(input())
        x.append(a)
        print('more delete columan then press C and for net file press D')
        moreDelete = str(input())
        if moreDelete == 'c' or moreDelete == 'C':
            pass
        elif moreDelete == 'd' or moreDelete == 'D':
            c = 2
         
        
    print("hjkkhkjafkjjjh",x)
    # res = [int(x) for a,x in enumerate(str(x))]
    # print("hghghgh",res)
    # x = x.split(",")
    # print("dfdfdfdf",x)
    
    df = df.drop(columns=df.columns[x])
    print(df)
    writer = pd.ExcelWriter(f'h/{uuid.uuid4()}.xlsx')
    # writer = (str(uuid.uuid1()) + "\n" for i in range(50))
 
    df.to_excel(writer)
    writer.save()
 
#############################


        if moreDelete == 'c' or moreDelete == 'C':
            pass
        elif moreDelete == 'd' or moreDelete == 'D':
            c = 2
         
        
    print("hjkkhkjafkjjjh",x)
    # res = [int(x) for a,x in enumerate(str(x))]
    # print("hghghgh",res)
    # x = x.split(",")
    # print("dfdfdfdf",x)
    
    df = df.drop(columns=df.columns[x])
    print(df)
    writer = pd.ExcelWriter(f'h/{uuid.uuid4()}.xlsx')
    # writer = (str(uuid.uuid1()) + "\n" for i in range(50))
 
    df.to_excel(writer)
    writer.save()
 
#############################

