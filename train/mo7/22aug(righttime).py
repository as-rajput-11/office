  
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


# def set_trains():
list1 = ''
list2 = ''
lt=[]
kl=[]
subtracted = list()
cur = conn.cursor()
# - d_capacity 
cur.execute("select ids from (select array_agg(train_id) as ids, d_capacity from train_rpt1 group by detraining_station, d_capacity) a where array_length(ids, 1) > 0")
rows = cur.fetchall()

for r in rows:
    cur.execute('select train_id,arrival_time,d_capacity,detraining_station,priority  from train_rpt1 where train_id in (' + ','.join(map(str, r[0])) + ') order by arrival_time')
    data = cur.fetchall()
    last_time = r,data[-1]
    lt.append(last_time)
    capacity=data[0][2]
    capacity_train_stop =[]
    capacity_train_on =[]
    cou = 0
    ft = int(math.ceil(capacity/2))

    for index,j in enumerate(data):
        if ft <= index:
            kl.append(j)
        else:
            continue

if kl == []:
    exit

sorted_list = sorted(
        kl, key=lambda t: t[4]
)

for i in sorted_list:
    print(i)


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

            po = neartostation[1] + datetime.timedelta(hours=12)
            do = neartostation[1] - datetime.timedelta(hours=12)
            

            cur.execute("select train_id, detraining_station from train_rpt1 where (arrival_time  between '"+str(do)+"' and '"+str(po)+"') and detraining_station = '"+str(near_station[0][1])+"'")
            zs = cur.fetchall()


            cur.execute("select capacity,station from mst_capacity where station =  '"+str(near_station[0][1])+"'")
            captostation=cur.fetchall()
            captostation1 = int(math.ceil((captostation[0][0])/2))
            countp = captostation1 - len(zs)
        

            if countp:
                # query down
                cur.execute("update trains set detraining_station ='"+str(captostation[0][1])+"' where train_id="+str(neartostation[0])+" ")
                
                conn.commit()
                near_station.clear()
            else:
                if len(near_station ) <= 1:
                    timingchange.append(neartostation)
                near_station.pop(0)
##################################################################################################################################                    

count = 0
for key, delay_time_list in itertools.groupby(timingchange, lambda x: x[3]):
        # Priority Logic
        delay_time_list = list(delay_time_list)
        # if delay_time_list == []:
        #     exit
        cur.execute("select  train_id,arrival_time +interval'12 hour ' as addtime ,detraining_station,priority,d_capacity from train_rpt1 where detraining_station = '"+str(key)+"' order by arrival_time ")
        data5 = cur.fetchall()
        delt = []
        id=[]
        cap = int(math.ceil(data5[0][4]/2))
        count += 1
        print(count,'count')
        for i in data5:
            print(i,'dataatattatattsdstdstdstd')
        print()
        print(len(delay_time_list),'llllllllllll')
        for i in delay_time_list:
            print(i,'delay_time_list11111111111111111111')
        print()
        for z in range(len(delay_time_list)):

            # for i in delay_time_list:
            #     print(i,'delay_time_list')
            # print()

            # def set_trains():
            for i in range(cap):
                if delay_time_list == [] or data5 == []:
                    break
                time_dif = data5[i][1]-delay_time_list[i][1]
                delt.append(delay_time_list[i])
                # [data5.remove(j) for j in data5 if j[0] == delay_time_list[i][0]]
                if delay_time_list == [] or data5 == []:
                    break
                data5[i] = delay_time_list[i]
                cur.execute("update trains set e_loading = e_loading +interval'"+str(time_dif)+"' where train_id= "+str(delay_time_list[i][0])+"")
                conn.commit()
            print()
            print(data5,'data5')
            print()
            for i in range(cap):
                id.append(data5[i][0])
            if id == []:
                break
            print(id,'iddd')

            cur.execute("select  train_id,arrival_time +interval'12 hour ' as addtime ,detraining_station,priority,d_capacity from train_rpt1 where train_id = any(array{t_id}) order by priority;".format(t_id=id))
            data5 = cur.fetchall()
            
            print(data5,'ffffffffffff')
            id=[]
            
            for i in delay_time_list:
                print(i,'delay_time_list2222222222222222222222222')
            print()

            [delay_time_list.remove(j) for i in delt for j in delay_time_list if i[0] == j[0]]
            delt = []

            for i in delay_time_list:
                print(i,'delay_time_list333333333333333333333333')
            print()

            if len(delay_time_list) < cap:
                cap = len(delay_time_list)
            
            for i in range(cap):
                    if delay_time_list == [] or data5 == []:
                        break

                    
                    time_dif = data5[i][1]-delay_time_list[i][1]
                    delt.append(delay_time_list[i])
                    # [data5.remove(j) for j in data5 if j[0] == delay_time_list[i][0]]
                    data5[i] = delay_time_list[i]
                    cur.execute("update trains set e_loading = e_loading +interval'"+str(time_dif)+"' where train_id= "+str(delay_time_list[i][0])+"")
                    conn.commit()
            print(data5,'ggggggggggggggggg')
            # if len(delay_time_list) <= cap:
            #     re=0
            # else:
            #     if delay_time_list == [] or data5 == []:
            #         break
            #     re = int(math.ceil(len(delay_time_list)/cap))

            # # for i in range(re):
            #     # list comprehension
            #     # [id.append(data5[i][0]) for i in range(re)]
            #     # for i in range(re):
            #     #     if len(data5) < i:
            #     #         break
            #     #     id.append(data5[i][0])
            #     [id.append(i[0]) for i in range(re) for i in data5]
            #     # print()
            #     # print(id,'iddddddddddddddddddddddddddiiiiiiiiiiiiiiiiiiiii')
            #     # print()
            #     cur.execute("select  train_id,arrival_time +interval'12 hour ' as addtime ,detraining_station,priority,d_capacity from train_rpt1 where train_id = any(array{t_id}) order by priority;".format(t_id=id))
            #     data5 = cur.fetchall()
            #     id=[]

            #     [delay_time_list.remove(j) for i in delt for j in delay_time_list if i[0] == j[0]]
            #     delt = []

            #     if len(delay_time_list) < cap:
            #         cap = len(delay_time_list)

            #     for i in range(cap):
            #         if delay_time_list == [] or data5 == []:
            #             break
            #         time_dif = data5[i][1]-delay_time_list[i][1]
            #         delt.append(delay_time_list[i])
            #         [data5.remove(j) for j in data5 if j[0] == delay_time_list[i][0]]
            #         data5[i] = delay_time_list[i]
            #         cur.execute("update trains set e_loading = e_loading +interval'"+str(time_dif)+"' where train_id= "+str(delay_time_list[i][0])+"")
            #         conn.commit()





# ##############################################################################################################################################################
#     if len(kl)>0:
#         set_trains()

# set_trains()

            # cur.execute("select ids from (select array_agg(train_id) as ids, d_capacity from train_rpt1 group by detraining_station, d_capacity) a where array_length(ids, 1) > 0")
            # rows = cur.fetchall()
            # kll = []
            # for r in rows:
            #     cur.execute('select train_id,arrival_time,d_capacity,detraining_station,priority  from train_rpt1 where train_id in (' + ','.join(map(str, r[0])) + ') order by arrival_time')
            #     data = cur.fetchall()
            #     last_time = r,data[-1]
            #     lt.append(last_time)
            #     capacity=data[0][2]
            #     capacity_train_stop =[]
            #     capacity_train_on =[]
            #     cou = 0
            #     ft = int(math.ceil(capacity/2))

            #     for index,i in enumerate(data):
            #         list1 = datetime.datetime.strptime(str(i[1]).split('.')[0],'%Y-%m-%d %H:%M:%S')
            #         capacity_train_stop.append(list1)

            #         if index >= ft:
            #             list2 = datetime.datetime.strptime(str(i[1]).split('.')[0],'%Y-%m-%d %H:%M:%S')
            #             capacity_train_on.append(list2)
            #             co =capacity_train_on[cou]-capacity_train_stop[cou] <= datetime.timedelta(hours=12)
            #             cou +=1
            #             if co == True:
            #                 kll.append(i)



            # sorted_list = sorted(
            #         kll, key=lambda t: t[4]
            # )
            # print()
            # for i in delt:
            #     print(i,'klllllllllkllllllllklllllllkll')
            # print()
            # for i in sorted_list:
            #     print(i,'sorteddddddddddddddddddddddddd')
                
            # # for i in delt:
            # #     for j in sorted_list:
            # #         print(i[0],j[0],'---------------------------------------------------------')
            # #         if i[0] == j[0]:
            # #             sorted_list.remove(j)
            # delt=[]
            # delay_time_list = sorted_list
            # print()
            # for i in delay_time_list:
            #     print(i,'bbbbbbbbbbbbbbbbbbbbbb')
            # print()
                                            
