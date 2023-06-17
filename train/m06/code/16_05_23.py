from flask import Flask, render_template, request, jsonify
import random, math, psycopg2
import datetime,json
import itertools
conn = psycopg2.connect(host='127.0.0.1', dbname= "postgres", user= "postgres", password= "postgres")
app = Flask(__name__)

@app.route('/')
def index():
    train_details = []
    cur = conn.cursor()
    try:
        postgres_select_query = "select \"nominal_odc\",\"entraning_station\",\"detraining_station\",\"consignment\",\"type\" from \"mst_select\" ORDER BY \"sr_no\" DESC"
        cur.execute(postgres_select_query)
    except Exception as e:
        print(e)    
    rows = cur.fetchall()
    cur.close()
    for r in rows:
        train_details.append({"nominal_odc" : r[0],"entraning_station" : r[1],"detraining_station" : r[2],"consignment" : r[3],"type" : r[4]})
    return render_template('index.html',train_details=train_details)

@app.route('/add_stations', methods=['GET'])
def add_stations():
    if request.method == "GET":
        stations = []
        cur = conn.cursor()
        try:
            postgres_select_query = "select \"station\" from \"mst_capacity\""
            cur.execute(postgres_select_query)
        except Exception as e:
            print(e)    
        rows = cur.fetchall()
        cur.close()
        for r in rows:
            stations.append({"station" : r[0]})
        return render_template('add_station.html',stations=stations)
        
@app.route('/save_stations', methods=['GET'])
def save_stations():
    if request.method == "GET":
        station = request.args.get('station')
        capacity = request.args.get('capacity')
        cur = conn.cursor()
        try: 
            cur.execute(f"insert into mst_capacity (station, capacity) values ('{station}', '{capacity}')")
        except Exception as e:
            print(e)
        conn.commit()
        res = cur.rowcount
        cur.close()
        if res == 0:
            return 'An Error Occured'
        else:
            return 'Data Saved Successfully'

@app.route('/stationdata_save')
def stationdata_save():
    id = request.args.get('id')
    from_station = request.args.get('from_station')
    to_station = request.args.get('to_station')
    distance = request.args.get('distance')
    cur = conn.cursor()
    try: 
        cur.execute(f"insert into mst_distance (src, dest, dist) values ('{from_station}', '{to_station}', '{distance}')")
    except Exception as e:
        print(e)
    conn.commit()
    res = cur.rowcount
    cur.close()
    if res == 0:
        return 'An Error Occured'
    else:
        return 'Data Saved Successfully'

@app.route('/data_save')
def data_save():
    train_id = request.args.get('train_id')
    nominal_odc = request.args.get('nominal_odc')
    entraning_station = request.args.get('entraning_station')
    start_time = request.args.get('start_time')
    detraining_station = request.args.get('detraining_station')
    consignment = request.args.get('consignment')
    type1 = request.args.get('type')
    cur = conn.cursor()
    if train_id == '0':
        try: 
            cur.execute(f"insert into trains (nominal_odc, entraning_station, start_time,detraining_station,consignment,type) values ('{nominal_odc}', '{entraning_station}', '{start_time}', '{detraining_station}', '{consignment}','{type1}')")
        except:
            pass
    else:
        try: 
            cur.execute(f"update trains set nominal_odc = '{nominal_odc}', entraning_station = '{entraning_station}', start_time = '{start_time}', detraining_station = '{detraining_station}', consignment = '{consignment}', type = '{type1}' where train_id = {train_id}")
        except:
            pass     
    conn.commit()
    res = cur.rowcount
    cur.close()
    if res == 0:
        return 'An Error Occured'
    else:
        return 'Data Saved Successfully'

@app.route('/traindetails')
def do_detail():
    train_detail = []
    cur = conn.cursor()
    try:
        cur.execute('select train_id, nominal_odc, entraning_station, start_time, detraining_station, consignment, type from trains order by train_id')
    except Exception as e:
        print(e)
    rows = cur.fetchall()
    cur.close()
    for r in rows:
        start_time = r[3].strftime('%d/%m/%Y %H:%M:%S')
        train_detail.append({"train_id": r[0], "nominal_odc": r[1], "entraning_station" : r[2], "start_time" : start_time, "detraining_station" : r[4], "consignment" : r[5], "type" : r[6]})
    return jsonify(train_detail)

@app.route('/reports')
def do_report():
    list1 = ''
    list2 = ''
    lt=[]
    kl=[]
    subtracted = list()
    cur = conn.cursor()
    cur.execute("select ids from (select array_agg(train_id) as ids, d_capacity from train_rpt group by detraining_station, d_capacity) a where array_length(ids, 1) - d_capacity > 0")
    rows = cur.fetchall()
    for r in rows:
        cur.execute('select train_id,arrival_time,d_capacity,detraining_station,priority  from train_rpt where train_id in (' + ','.join(map(str, r[0])) + ') order by arrival_time')
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
    print(kl,"=====================================================================")
    cur.execute("update trains set previous_time = NULL;")
    conn.commit

    for previous_time in kl:
        print(previous_time[0])
        cur.execute("update trains set previous_time = start_time where train_id ="+str(previous_time[0])+"")
        conn.commit()

    sorted_list = sorted(
            kl, key=lambda t: t[4]
    )
    print("++++++++",sorted_list)





    late_train=[]
    timingchange =[]  
    for neartostation in sorted_list:
        cur.execute("select * from mst_distance where src = '"+str(neartostation[3])+"' and dist < 70 order by dist")
        near_station = cur.fetchall()
        if near_station == []:
            timingchange.append(neartostation)
        else:
            while near_station :
                cur.execute("select detraining_station,d_capacity,arrival_time from train_rpt where detraining_station = '"+str(near_station[0][1])+"'")
                station0 = cur.fetchall()
                countp = len(station0)
                if station0[0][1] > countp:
                    cur.execute("update trains set detraining_station ='"+str(station0[0][0])+"' where train_id="+str(neartostation[0])+" ")
                    conn.commit()
                    near_station.clear()
                else:
                    if len(near_station ) <= 1:
                        timingchange.append(neartostation)
                    near_station.pop(0)
    for key, delay_time_list in itertools.groupby(timingchange, lambda x: x[3]):
        delay_time_list = list(delay_time_list)
        for item in range(len(delay_time_list)):
            cur.execute("select  train_id,arrival_time +interval'10 hour ' as addtime ,detraining_station from train_rpt where detraining_station = '"+str(key)+"' order by arrival_time ")
            data5 = cur.fetchall()
            # print(data4[item][1])
            time_dif = data5[item][1]-delay_time_list[item][1]
            cur.execute("update trains set start_time = start_time +interval'"+str(time_dif)+"' where train_id= "+str(delay_time_list[item][0])+"")
            conn.commit()
    report_detail = []
    cur = conn.cursor()
    try:
        cur.execute('select train_id, nominal_odc, type, entraning_station, start_time, detraining_station, consignment, speed, d_capacity, priority, distance, arrival_time, travel_time, loading_time from train_rpt order by train_id')
    except Exception as e:
        print(e)
    rows = cur.fetchall()
    cur.close()
    for r in rows:
        start_time = r[4].strftime('%d/%m/%Y %H:%M:%S')
        arrival_time = r[11].strftime('%d/%m/%Y %H:%M:%S')
        travel_time = str(r[12]).split('000')[0]
        loading_time = r[13].strftime('%d/%m/%Y %H:%M:%S')
        report_detail.append({"train_id": r[0],"nominal_odc": r[1],"type": r[2],"entraning_station": r[3],"start_time": start_time,"detraining_station": r[5],"consignment": r[6], "speed": r[7], "d_capacity" : r[8], "priority" : r[9], "distance" : r[10], "arrival_time" : arrival_time,"travel_time" : travel_time, "loading_time" : loading_time})
    return jsonify(report_detail)

@app.route('/report')
def do_reports():
    return render_template('reports.html')

@app.route('/checks')
def do_check():
    list1 = ''
    list2 = ''
    lt=[]
    kl=[]
    subtracted = list()
    cur = conn.cursor()
    cur.execute("DELETE FROM mst_check_late_train_details")
    cur.execute("select ids from (select array_agg(train_id) as ids, d_capacity from train_rpt group by detraining_station, d_capacity) a where array_length(ids, 1) - d_capacity > 0")
    rows = cur.fetchall()
    for r in rows:
        cur.execute('select train_id,arrival_time,d_capacity,detraining_station,loading_time,start_time ,priority from train_rpt where train_id in (' + ','.join(map(str, r[0])) + ') order by arrival_time')
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
    for check_late_train in kl:
        cur.execute(f"insert into mst_check_late_train_details(train_id,detraining_station,d_capacity,arrival_time,loading_time,start_time,priority) values("+str(check_late_train[0])+",'"+str(check_late_train[3])+"',"+str(check_late_train[2])+",'"+str(check_late_train[1])+"','"+str(check_late_train[4])+"','"+str(check_late_train[5])+"',"+str(check_late_train[6])+")")
        conn.commit()
        
    cur = conn.cursor()
    train_check_detail = []
    try:
        cur.execute('select train_id, detraining_station, d_capacity, start_time, arrival_time, loading_time,priority from mst_check_late_train_details order by train_id')
    except Exception as e:
        print(e)
    rows = cur.fetchall()
    cur.close()
    for r in rows:
        start_time = r[3].strftime('%d/%m/%Y %H:%M:%S')
        arrival_time = r[4].strftime('%d/%m/%Y %H:%M:%S')
        loading_time = r[5].strftime('%d/%m/%Y %H:%M:%S')
        train_check_detail.append({"train_id": r[0],"detraining_station": r[1],"d_capacity": r[2],"start_time": start_time,"arrival_time": arrival_time,"loading_time": loading_time,"priority":r[6]})
    return jsonify(train_check_detail)

@app.route('/check')
def do_checks():
    return render_template('train_check.html')

@app.route('/cluster')
def do_cluster():
    cur = conn.cursor()
    cur.execute("select array_agg(train_id) ,array_agg(entraning_station),detraining_station  from train_rpt  group by detraining_station ")
    detraining =cur.fetchall()
    for d_station in detraining:
    
        incoming = str(d_station[1])
        incoming = incoming.replace("[",'').replace("'",'').replace("]",'')
        incoming_id = str(d_station[0])
        incoming_id = incoming_id.replace("[",'').replace("'",'').replace("]",'')

    
        cur.execute("update mst_geojson_100km set in_coming_station ='"+str(incoming)+"', in_coming_id ='"+str(incoming_id)+"'  where station ='"+str(d_station[2])+"'")
        conn.commit()


    cur.execute("select array_agg(train_id),array_agg(detraining_station),entraning_station  from train_rpt  group by entraning_station")
    entraning = cur.fetchall()
    for e_station in entraning:

        outgoing = str(e_station[1])
        outgoing = outgoing.replace("[",'').replace("'",'').replace("]",'')
        outgoing_id = str(e_station[0])
        outgoing_id =outgoing_id.replace("[",'').replace("'",'').replace("]",'')
        cur.execute("update mst_geojson_100km set out_going_station ='"+str(outgoing)+"',out_going_id='"+str(outgoing_id)+"' where station ='"+str(e_station[2])+"'")
        conn.commit()

    cur.execute("select* from mst_geojson_100km order by id ")
    map_show_data = cur.fetchall()

    all_train = []
    for tup in map_show_data:
        all_train.append(tup)


    feature_collection = {
        "type": "FeatureCollection",
        "name": "rail",
        "features": []
    }

    for row in all_train:
        id, station_name, cap, y, x, point,in_c_id,in_c_s,out_id,out_s = row
        feature = {
            "type": "Feature",
            "properties": {
                "id": id,
                "station_name": station_name,
                "capacity": cap,
                "y": y,
                "x": x,
                "incoming_train_id": in_c_id,
                "incoming_train_station":in_c_s,
                "out_going_train_id": out_id,
                "out_going_train_station": out_s
            },
            "geometry": {
                "type": "Point",
                "coordinates": [x, y]
            }
        
        }
        
    
        feature_collection["features"].append(feature)


    print(json.dumps(feature_collection))

    jl = json.dumps(feature_collection)
    with open("/home/bisag/project work task_2023/vc/train_16_06_2023/static/demo1.geojson", mode="w") as f:
        json.dump(feature_collection, f)

    return render_template('cluster2.html')

if __name__ == '__main__':
    app.run(host= "0.0.0.0", debug= True, port=9000)
    
