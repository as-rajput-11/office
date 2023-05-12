# import pandas as pd 
# d = pd.read_excel('2.xlsx')
# print(d['destination_station'].to_string(index=False))


# # print(d['train_id'])
# # print(d)


# import pandas as pd
# from operator import *
# # Loading the Excel sheet into pandas DataFrame
# X = pd.read_excel('/home/bisag/project work task_2023/distance_m/del.xlsx')
# print(X)
# # print(j)

# from flask import Flask, render_template, request
# import psycopg2
# app = Flask(__name__)  
# # conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="localhost", port="5432")
# def get_data():
#     conn = psycopg2.connect(
#         host="localhost",
#         database="postgres",
#         user="postgres",
#         password="postgres")
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM trains')
#     data = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return data


# import psycopg2

# conn = psycopg2.connect(
#    database="postgres", user='postgres', password='postgres', host='localhost', port= '5432'
# )

# conn.autocommit = True
# cursor = conn.cursor()
# cursor.execute('''SELECT * from trains''')
# result = cursor.fetchone();
# print(result)
# result = cursor.fetchall();
# # print(result)
# conn.commit()
# conn.close()



import psycopg2
import datetime
import time

 
# Connect to the database
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
cur = conn.cursor()
cur.execute("select ids from (select array_agg(train_id) as ids, d_capacity from train_rpt group by detraining_station, d_capacity) a where array_length(ids, 1) - d_capacity > 0")
# cur.execute(" WITH a AS (SELECT r_trains.trains,r_trains.r_count FROM r_trains), b AS (SELECT train_rpt.train_id,train_rpt.nominal_odc,train_rpt.type,train_rpt.entraning_station,train_rpt.start_time,train_rpt.detraining_station,train_rpt.consignment,train_rpt.speed,train_rpt.d_capacity,train_rpt.priority,train_rpt.distance,train_rpt.arrival_time,train_rpt.travel_time FROM train_rpt) SELECT b.train_id, b.nominal_odc,   b.type, b.entraning_station,  b.start_time,b.detraining_station,b.consignment, b.speed,b.d_capacity,b.priority, b.distance,b.arrival_time,b.travel_time,a.trains, a.r_count FROM b,a WHERE b.train_id = ANY (a.trains) ORDER BY b.train_id;")
rows = cur.fetchall()

for r in rows:
   
    cur.execute('select train_id,arrival_time,d_capacity  from train_rpt where train_id in (' + ','.join(map(str, r[0])) + ') order by arrival_time')
    data = cur.fetchall()
  
    last_time = r,data[-1]
    lt.append(last_time)
    a = '2023-02-01 14:03:05'
    # date_format = "%H:%M:%S"
    kl=[]
    capacity=data[0][2]
    # print("===",data,capacity)
    capacity_train_stop =[]
    capacity_train_on =[]
    cou = 0
    # print("data",data)
    for index,i in enumerate(data):
     

        list1 = datetime.datetime.strptime(str(i[1]).split('.')[0],'%Y-%m-%d %H:%M:%S')
        capacity_train_stop.append(list1)


        
        if index >= capacity:

            list2 = datetime.datetime.strptime(str(i[1]).split('.')[0],'%Y-%m-%d %H:%M:%S')
            capacity_train_on.append(list2)
            co =capacity_train_on[cou]-capacity_train_stop[cou] < datetime.timedelta(hours=10)
           
               
            # print("jgjkgk",co)
            cou +=1
            if co == True:
               
                kl.append(i)
    
    for id in kl:
        print(id)
        id1 = id[0]
        cur.execute('select detraining_station from train_rpt where train_id = ('+str(id1)+') ')   
        data1  = cur.fetchall()
       
        data1 =  data1[0][0]

        # print("id",data1)
        cur.execute("select  arrival_time +interval'10 hour ' as addtime from train_rpt where detraining_station = '"+str(data1)+"' order by arrival_time asc limit 1 ")
        data2 = cur.fetchall()
        # print("data2",data2)
            
        update=datetime.datetime.strptime(str(id[1]).split('.')[0],'%Y-%m-%d %H:%M:%S')
        update1=datetime.datetime.strptime(str(data2[0][0]).split('.')[0],'%Y-%m-%d %H:%M:%S')
        timeupdate= update1-update
        # cur.execute("select start_time from trains where id = 3")
        # data3 = cur.fetchall()
        # print(data3)
        cur.execute("update trains set delay_time = start_time +interval'"+str(timeupdate)+"' where train_id= "+str(id1)+"")
        conn.commit()
        # print("update trains set start_time = start_time +interval'"+str(timeupdate)+"' where train_id= "+str(id1)+"")
            


    #     if list1 == '':
    #         list1 = datetime.datetime.strptime(str(i[1]).split('.')[0],'%Y-%m-%d %H:%M:%S')
    #         # print(data[1][1])
    #         # new_list = datetime.datetime.strptime(str(i[1]).split('.')[0],'%Y-%m-%d %H:%M:%S')
    #         # d = data[1][1]-list1 < datetime.timedelta(hours=10)
            
    #         # if d == True:
    #         #     # print(i)
    #         #     kl.append(data[1])
    
    #         # list1 = 'datetime.datetime('+(i[1])+')'
    #     else:
    #         # list2 = 'datetime.datetime('+(i[1])+')'
    #         list2 = datetime.datetime.strptime(str(i[1]).split('.')[0],'%Y-%m-%d %H:%M:%S')
     

    #         d = list2-list1 < datetime.timedelta(hours=10)
    #         print(d)
    #         if d == True:
    #             # print(i)
    #             kl.append(i)
    #         # if d < datetime.timedelta(hours=10):
    #         #     print(d )

    # list1 = ''
    # print('===================')
    # print("==jj",kl)

    # for id in kl:
   
    #     id1 = id[0]
    #     print(id1)
    
    #     cur.execute('select detraining_station from train_rpt where train_id = ('+str(id1)+') ')   
    #     data1  = cur.fetchall()
    #     print(data1)
    #     data1 =  data1[0][0]

    #     # print("id",data1)
    #     cur.execute("select  arrival_time +interval'10 hour ' as addtime from train_rpt where detraining_station = '"+str(data1)+"' order by arrival_time desc limit 1 ")
    #     data2 = cur.fetchall()
    #     print(id[1])
    #     print(data2[0][0])
    
    #     update=datetime.datetime.strptime(str(id[1]).split('.')[0],'%Y-%m-%d %H:%M:%S')
    #     update1=datetime.datetime.strptime(str(data2[0][0]).split('.')[0],'%Y-%m-%d %H:%M:%S')
    #     timeupdate= update1-update
    #     # cur.execute("select start_time from trains where id = 3")
    #     # data3 = cur.fetchall()
    #     # print(data3)
    #     cur.execute("update trains set delay_time = start_time +interval'"+str(timeupdate)+"' where train_id= "+str(id1)+"")
    #     conn.commit()
    #     print("update trains set start_time = start_time +interval'"+str(timeupdate)+"' where train_id= "+str(id1)+"")
    #     # print(id[2])


    # # cur.execute("select array_agg(train_id),max(arrival_time)+interval'10 hour'as addtime from public.with  group by detraining_station")
    # # add = cur.fetchall()

    # # print("sss",add)








        # print(r)   
cur.close()
conn.close()


























# l1=[]
# for dd in rows:
#     i = dd[0], dd[1], dd[2], dd[3], str(dd[4]), dd[5], dd[6], dd[7], dd[8], dd[9], dd[10], str(dd[11]), str(dd[12]),dd[13],dd[14]
#     l1.append(i)
# # l2=l1.count('PRAYAGRAJ')
# print(l1)

#     for l in i:
#         if l not in l1:
#             l1.append(i)
#     else:
#         print(i,end=' ')
    # print(dd[0], dd[1], dd[2], dd[3], dd[4], dd[5], dd[6], dd[7], dd[8], dd[9], dd[10], dd[11], dd[12], str(dd[13]),dd[14])
    # if  dd[5] in d:
        # duplicates.append(dd[5])
    # else:
        # d[dd[5]] = 1
# print('All the duplicates from list are :'+ str(duplicates))
        

