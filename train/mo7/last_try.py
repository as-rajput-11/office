
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
kl=[]

def trt():
    global   kl,cur
    list1 = ''
    list2 = ''
    lt=[]
    kl=[]
    subtracted = list()
    cur = conn.cursor()
    cur.execute("select ids from (select array_agg(train_id) as ids, d_capacity from train_rpt1 group by detraining_station, d_capacity) a where array_length(ids, 1)  > 0")
    rows = cur.fetchall()
    for r in rows:
        cur.execute('select train_id,arrival_time,d_capacity,detraining_station,priority  from train_rpt1 where train_id in (' + ','.join(map(str, r[0])) + ') order by arrival_time')
        data = cur.fetchall()
        last_time = r,data[-1]
        lt.append(last_time)
        # capacity=data[0][2]
        capacity=data[0][2]
        ft = int(math.ceil(capacity/2))
        capacity_train_stop =[]
        capacity_train_on =[]
        cou = 0
        for index,i in enumerate(data):
            list1 = datetime.datetime.strptime(str(i[1]).split('.')[0],'%Y-%m-%d %H:%M:%S')
            capacity_train_stop.append(list1)
            if index >= ft:
                list2 = datetime.datetime.strptime(str(i[1]).split('.')[0],'%Y-%m-%d %H:%M:%S')
                capacity_train_on.append(list2)
                # co =capacity_train_on[cou]-capacity_train_stop[cou] >= datetime.timedelta(hours=12,minutes=1)
                co =capacity_train_on[cou]-capacity_train_stop[cou] < datetime.timedelta(hours=12)


                cou +=1
                if co == True:
                    kl.append(i)

    sorted_list = sorted(
            kl, key=lambda t: t[4]
    )

    # print(sorted_list)

    if len(kl) > 0: 



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

        print(timingchange)
        for key, delay_time_list in itertools.groupby(timingchange, lambda x: x[3]):
                print(key)
                
                delay_time_list = list(delay_time_list)
                for i in range(len(delay_time_list)):
                    cur.execute("select  train_id,arrival_time +interval'12 hour ' as addtime ,detraining_station,priority,d_capacity from train_rpt1 where detraining_station = '"+str(key)+"' order by arrival_time ")
                    data5 = cur.fetchall()
                    print(key,delay_time_list)
                    time_dif = data5[i][1]-delay_time_list[i][1]
                    cur.execute("update trains set e_loading = e_loading +interval'"+str(time_dif)+"' where train_id= "+str(delay_time_list[i][0])+"")
                    conn.commit()

        list3 = ''
        list4 = ''
        lt1=[]
        kml=[]
        subtracted1 = list()
        cur = conn.cursor()
        cur.execute("select ids from (select array_agg(train_id) as ids, d_capacity from train_rpt1 group by detraining_station, d_capacity) a where array_length(ids, 1)  > 0")
        rows1 = cur.fetchall()
        for r in rows1:
            cur.execute('select train_id,arrival_time,d_capacity,detraining_station,priority  from train_rpt1 where train_id in (' + ','.join(map(str, r[0])) + ') order by arrival_time')
            data = cur.fetchall()
            last_time = r,data[-1]
            lt1.append(last_time)
            capacity=data[0][2]
            ft = int(math.ceil(capacity/2))
            capacity_train_stop =[]
            capacity_train_on =[]
            cou = 0
            for index,i in enumerate(data):
                list3 = datetime.datetime.strptime(str(i[1]).split('.')[0],'%Y-%m-%d %H:%M:%S')
                capacity_train_stop.append(list3)
                if index >= ft:
                    list4 = datetime.datetime.strptime(str(i[1]).split('.')[0],'%Y-%m-%d %H:%M:%S')
                    capacity_train_on.append(list4)
                    # co =capacity_train_on[cou]-capacity_train_stop[cou] >= datetime.timedelta(hours=12,minutes=1)
                    co =capacity_train_on[cou]-capacity_train_stop[cou] <= datetime.timedelta(hours=12)


                    cou +=1
                    if co == True:
                        kml.append(i)


        print(kml,"///")



        sorted_list = sorted(
                kml, key=lambda t: t[4]
        )

        print(sorted_list)


        for key, delay_time_list in itertools.groupby(sorted_list, lambda x: x[3]):
                # Priority Logic
            
                
                delay_time_list = list(delay_time_list)
                for i in range(len(delay_time_list)):
                    cur.execute("select  train_id,arrival_time +interval'12 hour ' as addtime ,detraining_station,priority,d_capacity from train_rpt1 where detraining_station = '"+str(key)+"' order by arrival_time ")
                    data6 = cur.fetchall()
                    print(key,delay_time_list)
                    time_dif = data6[i][1]-delay_time_list[i][1]
                    cur.execute("update trains set e_loading = e_loading +interval'"+str(time_dif)+"' where train_id= "+str(delay_time_list[i][0])+"")
                    conn.commit()

print(kl)
trt()


                                    
while kl != []:
    print('call while')
    trt()