import socket
from threading import Thread
from firebase import firebase 
import time
from unittest import result
import json
from urllib import request, parse
# from unittest import result

HOST = "192.168.1.3" 
PORT = 6969 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)
firebase = firebase.FirebaseApplication('https://project-iot-64a3a-default-rtdb.firebaseio.com/', None)

def make_param(data, data_humi):
    params = parse.urlencode({'field1': data, 'field2': data_humi}).encode()
    return params

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
        result = firebase.get('/raspberry/module-Relay', None)
        user_encode_data = json.dumps(result, indent=2).encode('utf-8')
        print(user_encode_data)
        conn.sendall(user_encode_data) 
        # time.sleep(1)
        
        conn.sendall(b"ON") 
        data_temp = conn.recv(1024)
        num_temp = data_temp.decode('utf-8')
        print("{}".format(num_temp))
        data_humi = conn.recv(1024)
        num_humi = data_humi.decode('utf-8')
        print("{}".format(num_humi))
        result1 = firebase.patch('/raspberry/sensor-DHT11',{'humidity': num_humi})
        result2 = firebase.patch('/raspberry/sensor-DHT11',{'temperature':num_temp})
        params_thingspeak = make_param(num_temp, num_humi)
        thingspeak_post(params_thingspeak)
        
        if not data_temp:
            break
        if not data_humi:
            break
        time.sleep(0.01)
        
        conn.sendall(b"ON_clock")
        data_minute = conn.recv(1024)
        num_minute = data_minute.decode('utf-8')
        print("{}".format(num_minute))
        data_second = conn.recv(1024)
        num_second = data_second.decode('utf-8')
        print("{}".format(num_second))
        result4 = firebase.patch('/raspberry/datetime',{'minute':num_minute})
        result5 = firebase.patch('/raspberry/datetime',{'second':num_second})
        if not data_second:
            break
        if not data_minute:
            break
        time.sleep(0.01)
        
        conn.sendall(b"ON_hour") 
        data_hour = conn.recv(1024)
        num_hour = data_hour.decode('utf-8')
        print("{}".format(num_hour))
        result3 = firebase.patch('/raspberry/datetime',{'hour':num_hour})
        if not data_hour:
            break
        time.sleep(0.01)
        
        conn.sendall(b"ON_sensor")
        data_sensor = conn.recv(1024)
        num_sensor = data_sensor.decode('utf-8')
        print("{}".format(num_sensor))
        num_int = float(num_sensor)
        if num_int >=3.0:
            print("Open the door")
            resultOpen = firebase.patch('/raspberry/distance',{'Door': dataOpen})
        else:
            print("Close the door")
            resultClose = firebase.patch('/raspberry/distance',{'Door': dataClose})
        
        
    print("End connection from {}".format(addr))
    conn.close()


while True:
    conn, addr = sock.accept()
    print("Got connection from {}".format(addr))
    Thread(target=new_client, args=(conn, addr)).start()
    