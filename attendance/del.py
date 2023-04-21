from flask import Flask, render_template, request
import psycopg2
app = Flask(__name__)  
conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="localhost", port="5432")

@app.route('/')  
def upload():  
    return render_template("index.html")  
 
@app.route('/success', methods = ['POST'])  
def success():  
    li =[]
    # global conn
    if request.method == 'POST':  
        f = request.files['file']   
        w = open(f.filename, "r")
        a = w.read()
        l = a.split('\n')
        cur = conn.cursor()
        cur.execute('delete from ad')
        for line in l:
            if(line.strip() != ""):
               b = line.split('\t')
               cur.execute(f"insert into ad(id_no,date,time) values({b[0].strip()}, '{b[1].split(' ')[0]}', '{b[1].split(' ')[1]}')")
            #    cur.close()
            conn.commit()
        cur = conn.cursor()
        cur.execute("select id_no, date, min(time) as in_time, max(time) as out_time from ad group by id_no, date order by id_no, date")
        data = cur.fetchall()
        ret_data = []
        for dd in data:
            # print(dd)
            ret_data.append({
                "id" : dd[0],
                "date": str(dd[1]),
                 "min": str(dd[2]),
                 "max": str(dd[3])
            })
        # li.append(data)
        # print(ret_data)
        return render_template("t.html",datas=ret_data)
  
if __name__ == '__main__':  
    app.run(debug = True)  