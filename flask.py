from flask import *  
app = Flask(__name__)  
 
@app.route('/')  
def upload():  
    return render_template("index.html")  
 
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']   
        # f.save(f.filename)
        r = f.filename
        w = open(r, "r")
        a = w.read()
        l = a.split('\n')
        d = []

        for line in l:
            if(line.strip() != ""):
               b = line.split('\t')
               d.append({
                "id" : b[0].strip(),
               "date" : b[1].split(' ')[0],
               "time" : b[1].split(' ')[1]
               })
        print(d)
        return render_template("t.html", name = f.filename)  
  
if __name__ == '__main__':  
    app.run(debug = True)  
    
    
    
    
    
   ###############
  <html>  
<head>  
    <title>upload</title>  
</head>  
<body>  
    <form action = "/success" method = "post" enctype="multipart/form-data">  
        <input type="file" name="file" />  
        <input type = "submit" value="Upload">  
    </form>  
</body>  
</html>  
###############


<html>  
<head>  
<title>success</title>  
</head>  
<body>  
<p>File uploaded successfully</p>  
<p>File Name: {{name}}</p>  
</body>  
</html>  
