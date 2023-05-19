import psycopg2
import datetime
import time
import itertools

conn = psycopg2.connect(
    database="postgres",
    user='postgres',
    password='postgres',
    host='localhost',
    port='5432'
)
list1 = ''
list2 = ''

lt=[]
kl=[]

subtracted = list()
cur = conn.cursor()
cur.execute("select ids from (select array_agg(train_id) as ids, d_capacity from train_rpt group by detraining_station, d_capacity) a where array_length(ids, 1) - d_capacity > 0")

rows = cur.fetchall()

for r in rows:
   
    cur.execute('select train_id,arrival_time,d_capacity,detraining_station  from train_rpt where train_id in (' + ','.join(map(str, r[0])) + ') order by arrival_time')
    data = cur.fetchall()
   
  
    last_time = r,data[-1]
    lt.append(last_time)
    
    

    capacity=data[0][2]
    
    capacity_train_stop =[]
    capacity_train_on =[]
    cou = 0
    
    for index,i in enumerate(data):
        list1 = datetime.datetime.strptime(str(i[1]).split('.')[0],'%Y-%m-%d %H:%M:%S')
        capacity_train_stop.append(list1)
        if index >= capacity:
            list2 = datetime.datetime.strptime(str(i[1]).split('.')[0],'%Y-%m-%d %H:%M:%S')
            capacity_train_on.append(list2)
            co =capacity_train_on[cou]-capacity_train_stop[cou] < datetime.timedelta(hours=10)
            cou +=1
            if co == True:
                kl.append(i)
 

late_train=[]




    
for k, g in itertools.groupby(kl, lambda x: x[3]):
        
     
        g = list(g)
     
        for item in range(len(g)):
            print(g)
            cur.execute("select  train_id,arrival_time +interval'10 hour ' as addtime ,detraining_station from train_rpt where detraining_station = '"+str(k)+"' order by arrival_time ")
            data4 = cur.fetchall()
          
            time_dif = data4[item][1]-g[item][1]
            print(time_dif)
            cur.execute("update trains set start_time = start_time +interval'"+str(time_dif)+"' where train_id= "+str(g[item][0])+"")
            conn.commit()
     

                        
