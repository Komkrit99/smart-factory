import sim
import json
from time import sleep
import urllib3
import threading
import time
import paho.mqtt.client as mqtt
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
key = ''
host = "test.mosquitto.org"
port = 8000
red = 'none'
r_n = 0
blue = 'none'
b_n = 0
green = 'none'
g_n = 0
purple = 'none'
p_n = 0
yellow = 'none'
y_n = 0
mode = ''
new_color = ''
new_sensor_0 = ''
id0 = 0
id1 = 0
id2 = 0
id3 = 0
id4 = 0
id5 = 0
id6 = 0
id7 = 0
id8 = 0
id9 = 0
app = FastAPI()
msg = 0
http = urllib3.PoolManager()
def updateleft():
    print('start')
    global red,r_n,blue,b_n,green,g_n,purple,p_n,yellow,y_n,mode
    r =requests.post('http://127.0.0.1:8000/left/', json={'r':r_n,'b':b_n,"g": g_n,'y':y_n,'p':p_n})
    r.status_code
    r.json()
def on_connect(self, client, userdata, rc):
    print("MQTT Connected.")
    self.subscribe("MQTT/SMF")

def on_message(client, userdata,msg):
    global key
    key = msg.payload.decode("utf-8")
    print(key)
    cn = 0
    global red,r_n,blue,b_n,green,g_n,purple,p_n,yellow,y_n,mode
    if key.split(',')[0] == 'add':
        mode = 'add'
        if key.split(',')[1].lower() == 'reset':
            red = 1
            r_n = 0
            blue = 2
            b_n = 0
            green = 3
            g_n = 0
            yellow = 4
            y_n = 0
            purple = 5
            p_n = 0
    
        else:
            red = 1
            r_n += int(key.split(',')[1])
            blue = 2
            b_n += int(key.split(',')[2])
            green = 3
            g_n += int(key.split(',')[3])
            yellow = 4
            y_n += int(key.split(',')[4])
            purple = 5
            p_n += int(key.split(',')[5])
        # print(red,r_n,blue,b_n,green,g_n,purple,p_n,yellow,y_n,mode)
        updateleft()
        # if r_n ==0 and b_n == 0 and g_n == 0 and y_n == 0 and p_n ==0:
        #     if key.split(',')[1] != '0':
        #         red = 1
        #         r_n += int(key.split(',')[1])
        #     if key.split(',')[2] != '0':
        #         blue = 2
        #         b_n += int(key.split(',')[2])
        #     if key.split(',')[3] != '0':
        #         green = 3
        #         g_n += int(key.split(',')[3])
        #     if key.split(',')[4] != '0':
        #         yellow = 4
        #         y_n += int(key.split(',')[4])
        #     if key.split(',')[5] != '0':
        #         purple = 5
        #         p_n += int(key.split(',')[5])
        # else:
        #     r_n += int(key.split(',')[1])
        #     b_n += int(key.split(',')[2])
        #     g_n += int(key.split(',')[3])
        #     y_n += int(key.split(',')[4])
        #     p_n += int(key.split(',')[5])
    elif key.split(',')[0] == 'set':
        mode = 'set'
        if key.split(',')[1] == 'reset':
            red = 'none'
            blue = 'none'
            green = 'none'
            purple = 'none'
            yellow = 'none'  
        else:
            if key.split(',')[1] == 'r':
                red = key.split(',')[2]
            if key.split(',')[1] == 'b':
                blue = key.split(',')[2]
            if key.split(',')[1] == 'g':
                green = key.split(',')[2]
            if key.split(',')[1] == 'y':
                yellow = key.split(',')[2]
            if key.split(',')[1] == 'p':
                purple = key.split(',')[2]       
def connect_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host)
    client.loop_forever()
client = connect_mqtt()
client.loop_forever()


def pusher(number,ping):
    updateste(number,2)
    sleep(ping)
    # Activate
    data_json = {"action": 1}
    data_encode = json.dumps(data_json).encode("utf-8")
    res = http.request("POST",
                       "http://localhost/tss/0/actuator/"+number,
                       body=data_encode,
                       headers={"Content-Type": "application/json"})
    text = res.data.decode("utf-8")
    sleep(0.6)
    # Deactivate
    data_json = {"action": 0}
    data_encode = json.dumps(data_json).encode("utf-8")
    res = http.request("POST",
                       "http://localhost/tss/0/actuator/"+number,
                       body=data_encode,
                       headers={"Content-Type": "application/json"})
    text = res.data.decode("utf-8")
    updateste(number,0)


def wait_Pusher(number):
    updateste(number,1)
    print('wait')
    old_num = '0'
    num_count = 0
    res = http.request( "GET",
                        "http://localhost/tss/0/latency"
                        )
    pings    = res.data.decode("utf-8")
    print(pings.split(',')[1].split(':')[1])
    ping = 1000/float(pings.split(',')[1].split(':')[1])
    while True:
        res = http.request("GET",
                           "http://localhost/tss/0/sensor/"+number
                           )
        num = res.data.decode("utf-8")

        if num[43] != old_num:
            old_num = num[43]
            print(old_num)
            num_count += 1
            threading.Thread(target=pusher ,args=num.split('"')[9])

            if num_count == 2:
                break
def updateste(number,ste):
    global id0,id1,id2,id3,id4,id5,id6,id7,id8,id9
    if int(number) == 0:
        id0 = ste
    if int(number) == 1:
        id1 = ste
    if int(number) == 2:
        id2 = ste
    if int(number) == 3:
        id3 = ste
    if int(number) == 4:
        id4 = ste
    if int(number) == 5:
        id5 = ste
    if int(number) == 6:
        id6 = ste
    if int(number) == 7:
        id7 = ste
    if int(number) == 8:
        id8 = ste
    if int(number) == 9:
        id9 = ste
    data_json = {'id0':id0,'id1':id1,'id2':id2,
    'id3':id3,'id4':id4,'id5':id5,
    'id6':id6,'id7':id7,'id8':id8,'id9':id9}
    data_encode = json.dumps(data_json).encode("utf-8")
    res = http.request("POST",
                       "http://127.0.0.1:8000/wait/",
                       body=data_encode,
                       headers={"Content-Type": "application/json"})
    text = res.data.decode("utf-8")




while True:
    
    res = http.request("GET",
                       "http://localhost/tss/0/sensor/0"
                       )
    sensor_0 = res.data.decode("utf-8")
    if new_sensor_0 != sensor_0[43]:
        new_sensor_0 = sensor_0[43]
        if new_sensor_0 == '1':
            res = http.request("GET",
                       "http://localhost/tss/0/sensor/10"
                       )
            color = res.data.decode("utf-8")

            new_color = color.split('"')[9]
            print(new_color)
            if mode == 'add':
                if new_color.lower() == 'red':

                    if r_n != 0 and red != 'none':
                        threading.Thread(target=wait_Pusher,args=red).start()
                        r_n -= 1
                        print(r_n,'Left')
                elif new_color.lower() == 'blue':
                    if b_n != 0  and blue != 'none':
                        threading.Thread(target=wait_Pusher,args=blue).start()
                        b_n -= 1
                        print(b_n,'Left')
                elif new_color.lower() == 'green':
                    if g_n != 0  and green != 'none':
                        threading.Thread(target=wait_Pusher,args=green).start()
                        g_n -= 1
                elif new_color.lower() == 'yellow':
                    if y_n != 0  and yellow != 'none':
                        threading.Thread(target=wait_Pusher,args=yellow).start()
                        y_n -= 1
                elif new_color.lower() == 'purple':
                    if p_n != 0  and purple != 'none':
                        threading.Thread(target=wait_Pusher,args=purple).start()
                        p_n -= 1
            if mode == 'set':
                if new_color.lower() == 'red':
                    if red != 'none':
                        threading.Thread(target=wait_Pusher,args=red).start()
                elif new_color.lower() == 'blue':
                    if blue != 'none':
                        threading.Thread(target=wait_Pusher,args=blue).start()
                elif new_color.lower() == 'green':
                    if green != 'none':
                        threading.Thread(target=wait_Pusher,args=green).start()
                elif new_color.lower() == 'yellow':
                    if yellow != 'none':
                        threading.Thread(target=wait_Pusher,args=yellow).start()
                elif new_color.lower() == 'purple':
                    if purple != 'none':
                        threading.Thread(target=wait_Pusher,args=purple).start()
            updateleft()

