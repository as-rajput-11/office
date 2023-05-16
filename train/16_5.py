
import psycopg2
import datetime
import time

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
   
    cur.execute('select train_id,arrival_time,d_capacity  from train_rpt where train_id in (' + ','.join(map(str, r[0])) + ') order by arrival_time')
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
 


sts = []
print(kl)
while len(kl) > 0:
#for id in kl:
    id = kl.pop(0)
    print(id)
    id1 = id[0]#2023-02-01 00:26:17
    cur.execute('select detraining_station from train_rpt where train_id = ('+str(id1)+') ')   
    data1  = cur.fetchall()
    data1 =  data1[0][0]
    cur.execute("select  train_id,arrival_time +interval'10 hour ' as addtime ,detraining_station from train_rpt where detraining_station = '"+str(data1)+"' order by arrival_time  ")
    data2 = cur.fetchall()
    train ='yes'
    #print("data2",data2)
    for index,fid in enumerate(data2):
        # if train == 'yes':
        if id1 == fid[0]:
            j =data2[index -1][1]
            print("first_condition",j)
            timed = datetime.datetime.strptime(str(data2[index -1][1]).split('.')[0],'%Y-%m-%d %H:%M:%S')
            timed2 = datetime.datetime.strptime(str(id[1]).split('.')[0],'%Y-%m-%d %H:%M:%S')
            timeupdate= timed-timed2
            print(timeupdate)
            cur.execute("update trains set delay_time = start_time +interval'"+str(timeupdate)+"' where train_id= "+str(id1)+"")
            #cur.execute("update trains set start_time = start_time +interval'"+str(timeupdate)+"' where train_id= "+str(id1)+"") 
            conn.commit()


    #     else:
       

    #         if id1 == fid[0]:
                
    #             j1 =data2[index -1][1]
    #             timed1 = datetime.datetime.strptime(str(data2[index -1][1]).split('.')[0],'%Y-%m-%d %H:%M:%S')

    #             timed3 = datetime.datetime.strptime(str(id[1]).split('.')[0],'%Y-%m-%d %H:%M:%S')
    #             timeupdate1= timed1-timed3
    #             print(timeupdate1)

    #             cur.execute("update trains set delay_time = start_time +interval'"+str(timeupdate1)+"' where train_id= "+str(id1)+"")
    #             conn.commit()
    # train ='no'




#########################################################################
            #     print(timeupdate,"jkbhdsfjklv")
                
                
            #     tim = 'bbb'
                
            # else:
                
                
            #     cur.execute("select train_id,delay_time + '01:00:00'::interval * (distance / speed::double precision) as update_time from train_rpt where train_id="+str(id1)+"")
            #     data3 = cur.fetchall()
            #     #print(data3[0][1],"edsthhtrery")

            #     su = datetime.datetime.strptime(str(data3[0][1]).split('.')[0],'%Y-%m-%d %H:%M:%S')
            #     su1 = datetime.datetime.strptime(str(id[1]).split('.')[0],'%Y-%m-%d %H:%M:%S')
                



            #     timeupdate= su-su1
            #     #print(timeupdate,"gjgjgjgjgjgj")

            # sid = id1
            
            
            
            
            



        
        
        
        
        
    
        
        






cur.close()
conn.close()








        
        
            
            



        
        
        

        
        
       




    
    
    
    
    
            
    
    
    
    
    
    
    
    
     

    
    
    
    
    
    
    

    
    
    

    
   
    
    
    
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


    
    

    














































    
    
        
    
        

        

