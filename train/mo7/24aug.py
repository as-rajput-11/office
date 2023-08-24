

import psycopg2
import datetime
import time
import itertools
import math

conn = psycopg2.connect(
    database="parth",
    user='postgres',
    password='postgres',
    host='localhost',
    port='5432'
)
cur = conn.cursor()



# a = [(3, 10, 'MIRZAPUR', 3, 1), (7, 11, 'MIRZAPUR', 2, 1), (19, 15, 'MIRZAPUR', 3, 1), (22, 16, 'MIRZAPUR', 3, 1)]
# b = [(19, 20, 'MIRZAPUR', 3, 1), (22, 40, 'MIRZAPUR', 3, 1),(23, 50, 'MIRZAPUR', 3, 1),(24, 55, 'MIRZAPUR', 3, 1)]
# d = [(19, 20, 'MIRZAPUR', 3, 1), (22, 40, 'MIRZAPUR', 3, 1),(23, 50, 'MIRZAPUR', 3, 1),(24, 55, 'MIRZAPUR', 3, 1)]
c =[]

# tt = 0



list1 = ''
list2 = ''
lt=[]
kl=[]
pl=[]
subtracted = list()
cur = conn.cursor()
cur.execute("select ids from (select array_agg(train_id) as ids, d_capacity from train_rpt1 group by detraining_station, d_capacity) a where array_length(ids, 1)  > 0")
rows = cur.fetchall()
for r in rows:
    cur.execute('select train_id,arrival_time,d_capacity,detraining_station,priority  from train_rpt1 where train_id in (' + ','.join(map(str, r[0])) + ') order by arrival_time')
    data = cur.fetchall()
    # print(data)
    
    last_time = r,data[-1]
    lt.append(last_time)
    capacity=data[0][2]
    capacity_train_stop =[]
    capacity_train_on =[]
    cou = 0
    for index,j in enumerate(data):
        if capacity <= index:
            kl.append(j)
        else:
            continue
sorted_list = sorted(
        kl, key=lambda t: [t[3],t[4]]
)
# print(sorted_list)

# print(kl,"=========+++++")

late_train=[]
timingchange =[]  
for neartostation in sorted_list:
    cur.execute("select * from mst_distance where src = '"+str(neartostation[3])+"' and dist <10 order by dist")
    near_station = cur.fetchall()
    cur.execute("select entraning_station,change_station from trains where train_id = '"+str(neartostation[0])+"'")
    near_e_station = cur.fetchall()
    
    near_e_station = [element for tupl in near_e_station for element in tupl]
    near_station = [item for item in near_station if all(elem not in item for elem in near_e_station)]
    

    


    if near_station == []:
        timingchange.append(neartostation)

    else:
        while near_station :
            cur.execute("select detraining_station,d_capacity,arrival_time from train_rpt1 where detraining_station = '"+str(near_station[0][1])+"'")
            station0 = cur.fetchall()
            print(station0)
            
            
            # countp = len(station0)
            
            cur.execute("select capacity,station from mst_capacity where station =  '"+str(near_station[0][1])+"'")
            captostation=cur.fetchall()
            countp = captostation[0][0] - len(station0)
            

            # if station0[0][1] > countp:
            if countp:
                # cur.execute("update trains set detraining_station ='"+str(station0[0][0])+"' where train_id="+str(neartostation[0])+" ")
                
                # query down
                cur.execute("update trains set detraining_station ='"+str(captostation[0][1])+"' where train_id="+str(neartostation[0])+" ")
                
                # conn.commit()
                near_station.clear()
            else:
                if len(near_station ) <= 1:
                    timingchange.append(neartostation)
                near_station.pop(0)
##################################################################################################################################                    

print(timingchange,"llllll")


for key, delay_time_list in itertools.groupby(timingchange, lambda x: x[3]):
        # Priority Logic
        delay_time_list = list(delay_time_list)
        
        cur.execute("select  train_id,arrival_time +interval'12 hour ' as addtime ,detraining_station,priority,d_capacity from train_rpt1 where detraining_station = '"+str(key)+"' order by arrival_time ")
        a = cur.fetchall()
        cap = a[0][4]
        test = cap
        b = delay_time_list 
        print(a,"------")
        print(" ")
        print(b,"late")
        tt=0

        for index,i in enumerate(b):
          
            if cap > index:
                print(a[index][0],b[index][0],'aaa')
                subi = (a[index][1]-b[index][1])

                cur.execute("update trains set e_loading = e_loading +interval'"+str(subi)+"' where train_id= "+str(b[index][0])+"")
                conn.commit()

            else:
                print(b[tt][0],"-----)))))))))_")
                cur.execute("select train_id ,d_loading_time from train_rpt1 where train_id = "+str(b[tt][0])+"")
                update =cur.fetchall()
                print(update)
                com = (update[0][1]-b[test][1])
                print(b[test][0])


                cur.execute("update trains set e_loading = e_loading +interval'"+str(com)+"' where train_id= "+str(b[test][0])+"")
                conn.commit()





                # print(com)
                # print(b[tt][0],b[test][0],'bbb')

                # print(b[tt][0],"------")

                # sub = (update[tt][1]- b[test][1])                
                test = test + 1
                tt = tt + 1

