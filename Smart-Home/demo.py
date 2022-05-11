import socket
from threading import Thread
from time import sleep
import numpy
import binascii
from urllib import request, parse
import json
import time

#HOST = "127.0.0.1" #(localhost)
HOST = "192.168.1.35" #Server IP
PORT = 65431 # Port to listen on
formatm = 'utf-8'
datas = []

#tao chuoi gui du lieu
def make_param(data1, data2, data3, data4):
    params = parse.urlencode({'field1': data1, 'field2': data2,'field3': data3 , 'field4': data4}).encode()
    return params

#gui du lieu len thingspeak
def thingspeak_post(params):
    api_key_write = "GFC99I663IPBBKR3"
    req = request.Request('https://api.thingspeak.com/update', method="POST")
    req.add_header("Content-type", "application/x-www-form-urlencoded")
    req.add_header('X-THINGSPEAKAPIKEY', api_key_write)
    r = request.urlopen(req, data=params)
    res_data = r.read()
    return res_data

#doc du lieu thingspeak de dieu khien thiet bi
def thingspeak_get():
    api_key_read = "3PE1CMQ1VNJXYARZ"
    channel_ID = "1666282"

    req = request.Request("https://api.thingspeak.com/channels/%s/fields/5/last.json?api_key=%s" %(channel_ID, api_key_read),method ="GET")
    r = request.urlopen(req)
    respone_data = r.read().decode()
    respone_data = json.loads(respone_data)
    value = respone_data["field5"]

    req1 = request.Request("https://api.thingspeak.com/channels/%s/fields/6/last.json?api_key=%s" %(channel_ID, api_key_read),method ="GET")
    r1 = request.urlopen(req1)
    respone_data1 = r1.read().decode()
    respone_data1 = json.loads(respone_data1)
    value1 = respone_data1["field6"]

    req2 = request.Request("https://api.thingspeak.com/channels/%s/fields/7/last.json?api_key=%s" %(channel_ID, api_key_read),method ="GET")
    r2 = request.urlopen(req2)
    respone_data2 = r2.read().decode()
    respone_data2 = json.loads(respone_data2)
    value2 = respone_data2["field7"]

    return [value, value1, value2]

def new_client(conn, addr):
    while True:
        
              
        data = conn.recv(1024).decode(formatm) #doc du lieu 
        datas.append(data)
        if not data:
            break

        if len(datas) == 4:
            data_temp = datas[0]
            data_humi = datas[1]
            data_light = datas[2]
            data_water = datas[3]
            params_thing= make_param(data_temp, data_humi, data_light, data_water)
            thingspeak_post(params_thing)
            print("Nhiet do: {} do, Do am: {}%".format(data_temp, data_humi))
            print("Do sang: {}".format(data_light))
            print("value water: {}".format(data_water))
            datas.clear()

            req_data = conn.recv(1024).decode(formatm)
            if req_data == "Req":
                #doc du lieu tu thingspeak
                value_c = thingspeak_get()
                v1 = "{}".format(value_c[0])
                v2 = "{}".format(value_c[1])
                v3 = "{}".format(value_c[2])
                #gui du lieu qua client
                send_v =[v1, v2, v3]
                for i in range(0,3):
                    conn.send(send_v[i].encode(formatm))
                    sleep(0.2)
            else:
                print("error")
        
         
    print("End connection from {}".format(addr))
    datas.clear()
    conn.close()


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the portc
sock.bind((HOST, PORT))
# Listen for incoming connections
sock.listen(1)
while True:
    conn, addr = sock.accept()
    print("Got connection from {}".format(addr))
    
    Thread(target=new_client, args=(conn, addr)).start()
    

    
    