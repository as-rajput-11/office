import random
import datetime
import radar
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
cur = conn.cursor()
station = ['VARANASI','GORAKHPUR','DDU_JUNCTION','PRAYAGRAJ','KANPUR','FATEHPUR','SHAHJAHANPUR','AGRA','ETAWAH','TUNDLA','LUCKNOW','MEERUT','MIRZAPUR',
        'BAREILLY','JAUNPUR','ALIGARH','HATHRAS','PRATAPGARH','GONDA','BASTI']
odc = ['A','B','C']
consignment = ['B','C','K','I','A','E','M','N','W','H','Z','D','SPL']
type= 'P'

for s in range(1,21):
    odc1 = random.choice(odc)
    consignment1 = random.choice(consignment)
    time_s=radar.random_date(start = datetime.datetime(year=2023, month=2, day=1), 
            stop = datetime.datetime(year=2023, month=2, day=4))
    # print(random.sample(station,2))
    station1 =random.sample(station,2)

    print(station1)
    ent_s=station1[0]
    des_s= station1[1]
    print("enter",station1[0])
    print(odc1,consignment1)
    print(time_s)
    print(type)
    print(s)
    cur.execute(f"INSERT INTO public.trains( train_id,nominal_odc, entraning_station, start_time, detraining_station, consignment, type) VALUES ('"+str(s)+"','"+str(odc1)+"', '"+str(ent_s)+"', '"+str(time_s)+"', '"+str(des_s)+"', '"+str(consignment1)+"', '"+str(type)+"')")
    conn.commit()

cur.close()
conn.close()



    
