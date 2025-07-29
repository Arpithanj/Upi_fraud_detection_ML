import mysql.connector, csv



link = mysql.connector.connect(
    host = 'localhost', 
    user = 'root', 
    password = '', 
    database = 'upifraud_2024'
)



def predictresult (data):
    result = '' 
    cursor = link.cursor() 
    cursor.execute("SELECT count(*) FROM upifraud_2024_history WHERE user = '"+data[3]+"'")
    print("SELECT count(*) FROM upifraud_2024_history WHERE user = '"+data[3]+"'")
    user = cursor.fetchone()
    print(user[0])
    if user[0] < 10:
        result = "Normal"
    else:
        cursor.execute("SELECT round(avg(amount)) as average FROM upifraud_2024_history WHERE user = '"+data[3]+"' ORDER BY id ASC LIMIT 10")
        print("SELECT round(avg(amount)) as average FROM upifraud_2024_history WHERE user = '"+data[3]+"' ORDER BY id ASC LIMIT 10")
        average = cursor.fetchone()
        #print(average[0])
        #print(data[2])
        input = int(data[2])
        avg = int(average[0])
        print(input)
        avg1=avg * 1.5
        print(avg1)
        if input > (avg * 1.5):
            result = "Fraud"
        else:
            result = "Normal" 

    return result





def fraudlist():
    
    data_array = []
    try:
        with open('fraudlist.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            data_array = [row[0] for row in csvreader if row]  
    except FileNotFoundError:
        data_array = []
    return data_array

 