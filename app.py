from flask import Flask, jsonify, redirect, render_template, request, session, url_for
import mysql.connector, random, string, os, csv
from predict import predictresult,fraudlist
import subprocess
import socket

app = Flask(__name__)
app.secret_key = "Qazwsx@123"  



link = mysql.connector.connect(
    host = 'localhost', 
    user = 'root', 
    password = '', 
    database = 'upifraud_2024'
)




@app.after_request
def add_header(response):
  
  response.cache_control.no_store = True
  return response




@app.route('/')
def index():
  
  return render_template('index.html')    




@app.route('/login', methods=['GET', 'POST'])
def login(): 
    
  if 'user' in session:
    return redirect(url_for('upload'))

  if request.method == "GET":
    return render_template('login.html') 
    
  else:
    cursor = link.cursor()
    try: 
      email = request.form["email"]
      password = request.form["password"]
      cursor.execute("SELECT * FROM upifraud_2024_user WHERE email = '"+email+"' AND password = '"+password+"'")
      user = cursor.fetchone()
      if user:
        session['user'] = user[3]
        session['username'] = user[2] 
        return redirect(url_for('upload'))
      else:
        return render_template('login.html', error='Invalid email or password') 
    
    except Exception as e:
      error = e
      return render_template('login.html', error=error)
      
    finally:
        cursor.close()     




@app.route('/forecast', methods=['GET', 'POST'])
def forecast(): 
    
  if 'user' not in session:
    return redirect(url_for('login'))
  
  cursor = link.cursor()
  try: 
    cursor.execute("SELECT * FROM upifraud_2024_predict limit 1000")
    data = cursor.fetchall()
    cursor.execute("SHOW COLUMNS FROM upifraud_2024_predict")
    columns = [column[0] for column in cursor.fetchall()] 
    link.commit()
    return render_template('forecast.html',data = data,columns = columns) 
    
  except Exception as e:
    error = e
    return render_template('error.html', error=error)
      
  finally:
    cursor.close()     





@app.route('/transactions', methods=['GET', 'POST'])
def transactions(): 
    
  if 'user' not in session:
    return redirect(url_for('login'))
  
  cursor = link.cursor()
  try: 
    cursor.execute("SELECT * FROM upifraud_2024_history limit 1000")
    data = cursor.fetchall()
    cursor.execute("SHOW COLUMNS FROM upifraud_2024_history")
    columns = [column[0] for column in cursor.fetchall()] 
    link.commit()
    return render_template('transactions.html',data = data,columns = columns) 
    
  except Exception as e:
    error = e
    return render_template('error.html', error=error)
      
  finally:
    cursor.close() 




@app.route('/register', methods=['GET', 'POST'])
def register():
      
  if 'user' in session:
    return redirect(url_for('upload'))

  if request.method == "GET": 
    return render_template('register.html') 
  
  else: 
    cursor = link.cursor()  
    try: 
      name = request.form["name"]
      email = request.form["email"]
      password = request.form["password"] 
      phone = request.form["phone"] 
      uid = 'uid_'+''.join(random.choices(string.ascii_letters + string.digits, k=10))
      cursor.execute("SELECT * FROM upifraud_2024_user WHERE email = '"+email+"'")
      user = cursor.fetchone()
 
      if user:
        return render_template('register.html', exists='Email already exists') 
      else:
        cursor.execute("INSERT INTO upifraud_2024_user (uid, name, email, password, phone) VALUES ('"+uid+"', '"+name+"', '"+email+"', '"+password+"', '"+phone+"')")
        link.commit()
        return render_template('register.html', success='Registration successful') 
       
    except Exception as e:
      error = e
      return render_template('register.html', error=error)
      
    finally:
        cursor.close() 




@app.route('/upload', methods=['GET', 'POST'])
def upload():

  if 'user' not in session:
    return redirect(url_for('login'))
  
  if request.method == "GET": 
    return render_template('upload.html') 

  else:
    cursor = link.cursor()
    try: 
      file = request.files["file"] 
      filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)) + '\\static\\docs', file.filename)
      file.save(filepath) 
      rows = []
        
      with open(filepath, 'r') as csvfile:
         csvreader = csv.reader(csvfile)  
         for row in csvreader:
           rows.append(row) 

      for row in rows[1:]: 
        if row and row[0] and row[0][0] != "":
          query=""
          query="insert into upifraud_2024_predict (uid,step,type,amount,nameorig,oldbalanceorg,newbalanceorig,namedest,oldbalancedest,newbalancedest,isfraud,isflaggedfraud) values ('uid_"+"".join(random.choices(string.ascii_letters + string.digits, k=10))+"',"

          for col in row: 
            query =query+"'"+col+"',"

          query =query[:-1]
          query=query+");"
          print(query)
          cursor.execute(query)
          link.commit()

      return render_template('upload.html', success='Upload successful', file=file.filename) 
    
    except Exception as e:
      error = e
      return render_template('error.html', error=error)
      
    finally:
        cursor.close() 





@app.route('/cleardataset', methods = ['POST'])
def cleardataset():

  if 'user' not in session:
    return redirect(url_for('login'))
  
  cursor = link.cursor()
  try: 
    query="delete from upifraud_2024_predict"
    cursor.execute(query) 
    link.commit()
    return render_template('upload.html', success='Dataset Cleared Successfully') 
  
  except Exception as e:
    error = e
    return render_template('error.html', error=error)
    
  finally:
      cursor.close() 




def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # Connect to an external address (e.g., Google DNS server)
        s.connect(('8.8.8.8', 80))
        ip_address = s.getsockname()[0]
    except Exception:
        ip_address = '127.0.0.1'
    finally:
        s.close()
    
    return ip_address




@app.route('/predict', methods=['GET', 'POST'])
def predict():

  if 'user' not in session:
    return redirect(url_for('login'))
  
  if request.method == "GET": 
    uid = 'uid_'+''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return render_template('predict.html', uid=uid) 

  else:
    cursor = link.cursor()
    try: 
      date = request.form["date"]
      time = request.form["time"]
      uid = request.form["uid"]
      sender = request.form["sender"]
      receiver = request.form["receiver"]
      amount = request.form["amount"]
      email = session["user"]
      result = predictresult([sender,receiver,amount,email])
      fraudlistarray = fraudlist()

      senderfraud = "no"
      receiverfraud = "no"

      cursor.execute("SELECT senderfraud,receiverfraud FROM upifraud_2024_history WHERE sender = '"+sender+"' or receiver = '"+sender+"' ORDER BY date DESC, time DESC LIMIT 1")
      senderfraudresult = cursor.fetchone()

      if senderfraudresult is not None and senderfraudresult[0] == "yes":
        senderfraud = "yes"
      
      if senderfraudresult is not None and senderfraudresult[1] == "yes":
        senderfraud = "yes"

      cursor.execute("SELECT senderfraud,receiverfraud FROM upifraud_2024_history WHERE receiver = '"+receiver+"' or sender = '"+receiver+"' ORDER BY date DESC, time DESC LIMIT 1")
      receiverfraudresult = cursor.fetchone()

      if receiverfraudresult is not None and receiverfraudresult[0] == "yes":
        receiverfraud = "yes"

      if receiverfraudresult is not None and receiverfraudresult[1] == "yes":
        receiverfraud = "yes"
        

      senderfraud = "yes" if sender in fraudlistarray else senderfraud
      receiverfraud = "yes" if receiver in fraudlistarray else receiverfraud

      
      if senderfraud == "yes" and receiverfraud == "yes":
          risk = "high risk"
      elif senderfraud == "yes" or receiverfraud == "yes":
          risk = "risk"
      else:
          risk = "normal"

      ipaddress = str(get_local_ip())

      print("INSERT INTO upifraud_2024_history (uid, user, username, date, time, sender, receiver, amount, result, ipaddress, senderfraud, receiverfraud, risk) VALUES ('"+uid+"', '"+email+"', '"+session["username"]+"', '"+date+"', '"+time+"', '"+sender+"', '"+receiver+"', '"+amount+"', '"+result+"', '"+ipaddress+"', '"+senderfraud+"', '"+receiverfraud+"', '"+risk+"')")

      cursor.execute("INSERT INTO upifraud_2024_history (uid, user, username, date, time, sender, receiver, amount, result, ipaddress, senderfraud, receiverfraud, risk) VALUES ('"+uid+"', '"+email+"', '"+session["username"]+"', '"+date+"', '"+time+"', '"+sender+"', '"+receiver+"', '"+amount+"', '"+result+"', '"+ipaddress+"', '"+senderfraud+"', '"+receiverfraud+"', '"+risk+"')")
      link.commit()

      print("----------------------------------------------")
      print(sender+"-"+receiver+"-"+amount+"-"+email)

      n = random.randint(123, 99999) 
      subprocess.run(["python", "blockmanager.py", "-s", sender+"-"+receiver+"-"+amount+"-"+email, "-r", str(n)])
      return render_template('result.html', result=result,risk=risk)
    
    except Exception as e:
      error = e
      return render_template('error.html', error=error)
      
    finally:
        cursor.close() 











@app.route('/check_fraud', methods=['POST'])
def check_fraud():
    data = request.get_json()
    email = data.get('email', '').strip()
    fraud_emails = fraudlist()
    exists = email in fraud_emails
    return jsonify({'exists': exists})








@app.route('/logout')
def logout():
    
    session.pop('user', None)
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == '__main__':
      app.run(debug=True)
