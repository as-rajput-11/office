import psycopg2
conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="localhost", port="5432")
cur = conn.cursor()
cur.execute('select distinct id_no from ad order by id_no')
d1 = cur.fetchall()
out = dict()
# mtmp = {'1':[],'2':[],'3':[],'4':[],'5':[],'6':[],'7':[],'8':[],'9':[],'10':[],'11':[],'12':[]}
for dd in d1:
    out[dd[0]] = []
cur.execute('select id_no, (array_agg(extract(month from date)))[1], date, min(time), max(time) from ad group by id_no, date')
d2 = cur.fetchall()
for dd in d2:
    temp = {
        "month": str(dd[1]),
        "date": str(dd[2]),
        "in": str(dd[3]),
        "out": str(dd[4])
    }
    out[dd[0]].append(temp)
print(out)
cur.close()
conn.close()