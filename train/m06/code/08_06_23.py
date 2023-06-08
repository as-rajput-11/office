import psycopg2 
conn = psycopg2.connect(host='127.0.0.1',dbname= "postgres",user ="postgres",password ="postgres" ,port= '5432')
cur =conn.cursor()
cur.execute("select array_agg(train_id) ,array_agg(entraning_station),detraining_station  from train_rpt  group by detraining_station ")
detraining =cur.fetchall()
for d_station in detraining:
   
    incoming = str(d_station[1])
    incoming = incoming.replace("[",'').replace("'",'').replace("]",'')
    incoming_id = str(d_station[0])
    incoming_id = incoming_id.replace("[",'').replace("'",'').replace("]",'')

    # print("update mst_geojson_100km set in_coming_station ='"+str(incoming)+"' ,in_coming_id ='"+str(incoming_id)+"'  where station ='"+str(d_station[2])+"'")
    cur.execute("update mst_geojson_100km set in_coming_station ='"+str(incoming)+"', in_coming_id ='"+str(incoming_id)+"'  where station ='"+str(d_station[2])+"'")
    conn.commit()

print("=========================")
cur.execute("select array_agg(train_id),array_agg(detraining_station),entraning_station  from train_rpt  group by entraning_station")
entraning = cur.fetchall()
for e_station in entraning:
    # print(e_station)
    outgoing = str(e_station[1])
    outgoing = outgoing.replace("[",'').replace("'",'').replace("]",'')
    outgoing_id = str(e_station[0])
    outgoing_id =outgoing_id.replace("[",'').replace("'",'').replace("]",'')
    cur.execute("update mst_geojson_100km set out_going_station ='"+str(outgoing)+"',out_going_id='"+str(outgoing_id)+"' where station ='"+str(e_station[2])+"'")
    conn.commit()

cur.execute("select* from mst_geojson_100km order by id ")
map_show_data = cur.fetchall()
# print(map_show_data)
for tup in map_show_data:
    new_tup = tuple(filter(lambda x: x is not None,tup))
    print(new_tup)

# for show in map_show_data:
#     print(show)
