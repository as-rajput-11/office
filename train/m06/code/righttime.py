
##################################################################################################################################################
     
import psycopg2
import datetime
import time
import itertools
from colorama import Fore, Back, Style 
from termcolor import colored,cprint

conn = psycopg2.connect(
    database="postgres1",
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

sorted_list = sorted(
            kl, key=lambda t: t[6]
    )

# print(sorted_list)









timingchange =[]  
for neartostation in sorted_list:
    cur.execute("select * from mst_distance where src = '"+str(neartostation[3])+"' and dist < 20 order by dist")
    near_station = cur.fetchall()

   
    # print(near_station)

    if near_station == []:
        timingchange.append(neartostation)
    
    else:
        blank =[]
        dict11 = dict()
        count_id = 0
        while near_station :
           
            cur.execute("select detraining_station,d_capacity,arrival_time from train_rpt where detraining_station = '"+str(near_station[0][1])+"'")
            station0 = cur.fetchall()
            
            cur.execute("select capacity,station from mst_capacity where station =  '"+str(near_station[0][1])+"'")
            captostation=cur.fetchall()
            # print(captostation,len(station0))
            


            # captostation=int(''.join(map(str, captostation[0][0])))
          
            countp = captostation[0][0] - len(station0)
            print("Available Capacity",countp,"Station",captostation[0][1],"Distance",near_station[0][2])
            

            if countp:
                count_id = count_id + 1
                dict11[count_id]= captostation[0][1]
                # print(dict11)
                # print(count_id)

                near_station.pop(0)
            else:

                if len(near_station ) <= 1:
                    # print("test")
                    timingchange.append(neartostation)
                near_station.pop(0)

      
        print("Index code And Station : ",dict11)
        # print("enter the near station : ")
        print(Fore.RED+"Train Id",neartostation[0],"And Detraining_Station",neartostation[3])

        near_u = input(Fore.YELLOW+"Enter The Redirection Station index_Code: ")
        near_u = near_u.replace(' ', '')
        near_u = int(near_u)
        print(Fore.WHITE+dict11[near_u])

        cur.execute("update trains set detraining_station ='"+str(dict11[near_u])+"' where train_id="+str(neartostation[0])+" ")
        # conn.commit()
        print("=================================================================================================")



for key, delay_time_list in itertools.groupby(timingchange, lambda x: x[3]):
        delay_time_list = list(delay_time_list)
       
        right =[]
        # print(timingchange)
        print(key,delay_time_list)


        for righttime in timingchange:
            # print(righttime[0])
            right.append(righttime[0])
        # print(right)
        right = tuple(right)
        cur.execute("select * from train_rpt where train_id  not in "+str(right)+" and detraining_station = '"+str(key)+"' ")
        righttrain = cur.fetchall()
        print(righttrain)
        



        # for item in range(len(delay_time_list)):
        #     cur.execute("select  train_id,arrival_time +interval'10 hour ' as addtime ,detraining_station from train_rpt where detraining_station = '"+str(key)+"' order by arrival_time ")
        #     data5 = cur.fetchall()
        #     print(data5)


            # time_dif = data5[item][1]-delay_time_list[item][1]
            # time_dif = re[item][1]-delay_time_list[item][1]

            
            # cur.execute("update trains set start_time = start_time +interval'"+str(time_dif)+"' where train_id= "+str(delay_time_list[item][0])+"")
            # conn.commit()

cur.execute("select entraning_station from train_rpt")
show_data_in_map = cur.fetchall()
# print(show_data_in_map)
