import socket
from threading import Thread
from time import sleep
from firebase import firebase 
import time
from unittest import result
import json
from urllib import request, parse

HOST = "192.168.1.3" 
PORT = 6969 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen()
firebase = firebase.FirebaseApplication('https://project-iot-64a3a-default-rtdb.firebaseio.com/', None)
formatm = 'utf-8'
datas = []

#tao chuoi gui du lieu
def make_param(data, data_humi):
    params = parse.urlencode({'field1': data, 'field2': data_humi}).encode()
    return params

#gui du lieu len thingspeak
def thingspeak_post(params):
    api_key_write = "9RLMQGFFN3E3HSCP"
    req = request.Request('https://api.thingspeak.com/update', method="POST")
    req.add_header("Content-type", "application/x-www-form-urlencoded")
    req.add_header('X-THINGSPEAKAPIKEY', api_key_write)
    r = request.urlopen(req, data=params)
    res_data = r.read()
    return res_data

dataOpen = {
    'this':'Open The Door'
}
dataClose = {
    'this':'Close The Door'
}


def new_client(conn, addr):
    
    while True:
            
        conn.sendall("ON".encode())      
        data = conn.recv(1024).decode(formatm) #doc du lieu 
        data = json.loads(data)
        if len(data) == 6:
            num_temp = data[0]
            num_humi = data[1]
            num_hour = data[2]
            num_minute = data[3]
            num_second = data[4]
            num_distance = data[5]
        params_thing= make_param(num_temp, num_humi)
        thingspeak_post(params_thing)
        result1 = firebase.patch('/raspberry/sensor-DHT11',{'humidity': num_humi})
        result2 = firebase.patch('/raspberry/sensor-DHT11',{'temperature':num_temp})
        result3 = firebase.patch('/raspberry/datetime',{'hour':num_hour})
        result4 = firebase.patch('/raspberry/datetime',{'minute':num_minute})
        result5 = firebase.patch('/raspberry/datetime',{'second':num_second})
        print("Nhiet do: {} do, Do am: {}%".format(num_temp, num_humi))
        print("{}:{}:{}".format(num_hour, num_minute, num_second))
        print("{}".format(num_distance))
        if num_distance >=3.0:
            print("Open the door")
            resultOpen = firebase.patch('/raspberry/distance',{'Door': dataOpen})
        else:
            print("Close the door")
            resultClose = firebase.patch('/raspberry/distance',{'Door': dataClose})
        time.sleep(0.1)
        if not data:
            break
        
        result = firebase.get('/raspberry/module-Relay', None)
        user_encode_data = json.dumps(result, indent=2)
        # print(user_encode_data)
        conn.sendall(user_encode_data.encode()) 
        
        
         
    print("End connection from {}".format(addr))
    conn.close()
 

while True:
    conn, addr = sock.accept()
    print("Got connection from {}".format(addr))
    
    Thread(target=new_client, args=(conn, addr)).start()

    
    