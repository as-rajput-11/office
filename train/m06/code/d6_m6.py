
##################################################################################################################################################
     
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
cur.execute("DELETE FROM mst_check_late_train_details")

for r in rows:
   
    # cur.execute('select train_id,arrival_time,d_capacity,detraining_station,priority  from train_rpt where train_id in (' + ','.join(map(str, r[0])) + ') order by arrival_time')
    cur.execute('select train_id,arrival_time,d_capacity,detraining_station,loading_time,start_time,priority  from train_rpt where train_id in (' + ','.join(map(str, r[0])) + ') order by arrival_time')
    
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

print(kl)

###########priority##################################################################################
cur.execute("delete from mst_running_train_priority ")
conn.commit
for check_priority in kl:
    cur.execute("insert into mst_running_train_priority(train_id, arrival_time,detraining_station, priority)VALUES("+str(check_priority[0])+",'"+str(check_priority[1])+"','"+str(check_priority[3])+"',"+str(check_priority[6])+")")
    conn.commit()
cur.execute("select * from mst_running_train_priority order by priority asc")
priority_train = cur.fetchall()

# print(priority_train,"+++++++++++")




######################################################################################################







timingchange =[]  
for neartostation in kl:

    cur.execute("select * from mst_distance where src = '"+str(neartostation[3])+"' and dist < 50 order by dist")
    near_station = cur.fetchall()
   
    
    if near_station == []:
        timingchange.append(neartostation)

    else:
        while near_station :
            
            cur.execute("select detraining_station,d_capacity,arrival_time from train_rpt where detraining_station = '"+str(near_station[0][1])+"'")
            station0 = cur.fetchall()
            # print("++++++++++++",station0)
            countp = len(station0)
            
                
            if station0[0][1] > countp:
                cur.execute("update trains set detraining_station ='"+str(station0[0][0])+"' where train_id="+str(neartostation[0])+" ")
                conn.commit()
                near_station.clear()
            else:
                if len(near_station ) <= 1:
                    print("test")
                    timingchange.append(neartostation)
                near_station.pop(0)


# print(timingchange)



for key, delay_time_list in itertools.groupby(timingchange, lambda x: x[3]):
        delay_time_list = list(delay_time_list)
       
        for item in range(len(delay_time_list)):
            print("==========================",key,delay_time_list[item][1])
    
            cur.execute("select  train_id,arrival_time +interval'10 hour ' as addtime ,detraining_station from train_rpt where detraining_station = '"+str(key)+"' order by arrival_time ")
            data5 = cur.fetchall()
            # print(data4[item][1])
         
          
            time_dif = data5[item][1]-delay_time_list[item][1]
            
            cur.execute("update trains set start_time = start_time +interval'"+str(time_dif)+"' where train_id= "+str(delay_time_list[item][0])+"")
            conn.commit()
     
