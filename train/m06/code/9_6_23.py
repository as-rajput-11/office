import psycopg2 
import json
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

all_train = []
for tup in map_show_data:
    new_tup = tuple(filter(lambda x: x is not None,tup))
    all_train.append(new_tup)





    # new_tup=str(new_tup)
    # print(type(new_tup))
    # print(new_tup[1])


features = []

for d in all_train:
    # print(d)
    properties = {
        "id": d[0],
        "name": d[1],
        "type_id": d[2],
        "latitude": d[3],
        "longitude": d[4],
        "zone_point": d[5]
    }
    
    if len(d) > 6:
        properties["in_id"] = d[6]
        
    if len(d) > 7:
        properties["in_s_name"] = d[7]
        
    if len(d) > 8:
        properties["out_ids"] = [int(x) for x in d[8].split(",")]
        
    if len(d) > 9:
        properties["out_s_names"] = [x.strip() for x in d[9].split(",")]
    
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [d[4], d[3]]
        },
        "properties": properties
    }
    
    features.append(feature)

geojson_data = {
    "type": "FeatureCollection",
    "features": features
}

# print(json.dumps(geojson_data))
# jl = json.dumps(geojson_data)
with open("demo.geojson", mode="w") as f:
    json.dump(geojson_data, f)
