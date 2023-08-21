
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
        kl, key=lambda t: t[4]
)
# print(sorted_list)



late_train=[]
timingchange =[]  
for neartostation in sorted_list:
    cur.execute("select * from mst_distance where src = '"+str(neartostation[3])+"' and dist <20 order by dist")
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
            
            
            # countp = len(station0)
            
            cur.execute("select capacity,station from mst_capacity where station =  '"+str(near_station[0][1])+"'")
            captostation=cur.fetchall()
            countp = captostation[0][0] - len(station0)
            

            # if station0[0][1] > countp:
            if countp:
                # cur.execute("update trains set detraining_station ='"+str(station0[0][0])+"' where train_id="+str(neartostation[0])+" ")
                
                # query down
                cur.execute("update trains set detraining_station ='"+str(captostation[0][1])+"' where train_id="+str(neartostation[0])+" ")
                
                conn.commit()
                near_station.clear()
            else:
                if len(near_station ) <= 1:
                    timingchange.append(neartostation)
                near_station.pop(0)
##################################################################################################################################                    


for key, delay_time_list in itertools.groupby(timingchange, lambda x: x[3]):
        # Priority Logic
        delay_time_list = list(delay_time_list)
        
        cur.execute("select  train_id,arrival_time +interval'12 hour ' as addtime ,detraining_station,priority,d_capacity from train_rpt1 where detraining_station = '"+str(key)+"' order by arrival_time ")
        data5 = cur.fetchall()
        delt = []
        id=[]
        cap = data5[0][4]  
        # cap = ft
        
        # print(cap,"12455555")
        if cap == 1:
            
            for i in range(cap):

                match_a =delay_time_list[0]
                data53 =[item for item in data5 if item[0] != match_a[0]]
                

                # print(delay_time_list,"update")
                
                time_dif = data53[i][1]-delay_time_list[i][1]

                
                delt.append(delay_time_list[i])
                [data5.remove(j) for j in data5 if j[0] == delay_time_list[i][0]]
                data5[i] = delay_time_list[i]
                cur.execute("update trains set e_loading = e_loading +interval'"+str(time_dif)+"' where train_id= "+str(delay_time_list[i][0])+"")
                conn.commit()
            
            if len(delay_time_list) <= cap:
                re=0
            else:
                re = int(math.ceil(len(delay_time_list)/cap))
            for i in range(re):
                for i in data5:
                    id.append(i[0])

                # cur.execute("select  train_id,arrival_time +interval'12 hour ' as addtime ,detraining_station,priority,d_capacity from train_rpt where detraining_station = '"+str(key)+"' order by arrival_time ")

                cur.execute("select  train_id,arrival_time +interval'12 hour ' as addtime ,detraining_station,priority,d_capacity from train_rpt1 where train_id = any(array{t_id}) order by priority;".format(t_id=id))
                data5 = cur.fetchall()
                id=[]
                for i in delt:
                    for j in delay_time_list:
                        if i[0] == j[0]:
                            delay_time_list.remove(j)
                delt=[]

                if delay_time_list == []:
                    break
                if len(delay_time_list) < cap:
                    cap = len(delay_time_list)

                for i in range(cap):
                    if data5[i][1] == delay_time_list[i][1]:
                        print(data5[i][1],delay_time_list[i][1],'samkkkkkkkkkkkkkkkkkkkkkkkk 22222222222')
                    print(delay_time_list,"step 2")

                    match_a =delay_time_list[0]
                    print(match_a,"22")
                    data53 =[item for item in data5 if item[0] != match_a[0]]


                    time_dif = data53[i][1]-delay_time_list[i][1]
                    delt.append(delay_time_list[i])
                    [data5.remove(j) for j in data5 if j[0] == delay_time_list[i][0]]
                    data5[i] = delay_time_list[i]
                    cur.execute("update trains set e_loading = e_loading +interval'"+str(time_dif)+"' where train_id= "+str(delay_time_list[i][0])+"")
                    conn.commit()

        else:
             
            for i in range(cap):
                print(data5,"old")

                match_a =delay_time_list[0]
                print(match_a,"op")
                data53 =[item for item in data5 if item[0] != match_a[0]]
                print(data53)
                

                # print(delay_time_list,"update")
                
                time_dif = data5[i][1]-delay_time_list[i][1]

                
                delt.append(delay_time_list[i])
                [data5.remove(j) for j in data5 if j[0] == delay_time_list[i][0]]
                data5[i] = delay_time_list[i]
                cur.execute("update trains set e_loading = e_loading +interval'"+str(time_dif)+"' where train_id= "+str(delay_time_list[i][0])+"")
                # conn.commit()
            
            if len(delay_time_list) <= cap:
                re=0
            else:
                re = int(math.ceil(len(delay_time_list)/cap))
            for i in range(re):
                for i in data5:
                    id.append(i[0])

                # cur.execute("select  train_id,arrival_time +interval'12 hour ' as addtime ,detraining_station,priority,d_capacity from train_rpt where detraining_station = '"+str(key)+"' order by arrival_time ")

                cur.execute("select  train_id,arrival_time +interval'12 hour ' as addtime ,detraining_station,priority,d_capacity from train_rpt1 where train_id = any(array{t_id}) order by priority;".format(t_id=id))
                data5 = cur.fetchall()
                id=[]
                for i in delt:
                    for j in delay_time_list:
                        if i[0] == j[0]:
                            delay_time_list.remove(j)
                delt=[]

                if delay_time_list == []:
                    break
                if len(delay_time_list) < cap:
                    cap = len(delay_time_list)

                for i in range(cap):
                    if data5[i][1] == delay_time_list[i][1]:
                        print(data5[i][1],delay_time_list[i][1],'samkkkkkkkkkkkkkkkkkkkkkkkk 22222222222')
                    print(delay_time_list,"step 2")

                    match_a =delay_time_list[0]
                    print(match_a,"22")
                    data53 =[item for item in data5 if item[0] != match_a[0]]


                    time_dif = data5[i][1]-delay_time_list[i][1]
                    delt.append(delay_time_list[i])
                    [data5.remove(j) for j in data5 if j[0] == delay_time_list[i][0]]
                    data5[i] = delay_time_list[i]
                    cur.execute("update trains set e_loading = e_loading +interval'"+str(time_dif)+"' where train_id= "+str(delay_time_list[i][0])+"")
                    # conn.commit()
