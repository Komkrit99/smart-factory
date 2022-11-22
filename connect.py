import sim
import json
from time import sleep
import urllib3
import threading
http = urllib3.PoolManager()
print("Program started")
sim.simxFinish(-1)
clientID = sim.simxStart('127.0.0.1', 19997, True, True, 5000, 5)


def connect():
    if clientID != -1:
        print("Connected")
        sim.simxAddStatusbarMessage(
            clientID, 'Hello CoppeliaSim!', sim.simx_opmode_oneshot)
    else:
        print("Not Connected")


def fromPython(msg):
    print(msg)
    inputInts = []
    inputFloats = []
    inputStrings = msg
    inputBuffer = bytearray()
    res, retInts, retFloats, retStrings, retBuffer = sim.simxCallScriptFunction(
        clientID, 'ConveyorBelt', sim.sim_scripttype_childscript, 'fromPython', inputInts, inputFloats, inputStrings, inputBuffer, sim.simx_opmode_blocking)
    sim.simxAddStatusbarMessage(clientID, 'finish!', sim.simx_opmode_oneshot)
    print('sented')


def pusher(number):

    # Activate
    data_json = {"action": 1}
    data_encode = json.dumps(data_json).encode("utf-8")
    res = http.request("POST",
                       "http://localhost/tss/0/actuator/"+number,
                       body=data_encode,
                       headers={"Content-Type": "application/json"})
    text = res.data.decode("utf-8")
    sleep(0.5)
    # Deactivate
    data_json = {"action": 0}
    data_encode = json.dumps(data_json).encode("utf-8")
    res = http.request("POST",
                       "http://localhost/tss/0/actuator/"+number,
                       body=data_encode,
                       headers={"Content-Type": "application/json"})
    text = res.data.decode("utf-8")
    # if number == '1':
    #     r.kill()
    # elif number == '2':
    #     b.kill()
    # elif number == '3':
    #     g.kill()
    # elif number == '4':
    #     y.kill()
    # elif number == '5':
    #     p.kill()

def wait_Pusher(number):
    print('start wait')
    old_num = '0'
    while True:
        res = http.request("GET",
                           "http://localhost/tss/0/sensor/"+number
                           )
        num = res.data.decode("utf-8")

        if num[43] != old_num:
            old_num = num[43]
            print(old_num)
        #     threading.Thread(target=pusher ,args=num.split('"')[9])
            
            break
    print('breal')
    pusher(number)



new_color = ''
new_sensor_0 = ''
r = threading.Thread(target=wait_Pusher,args='1')
b = threading.Thread(target=wait_Pusher,args='2')
g =threading.Thread(target=wait_Pusher,args='3')
y =threading.Thread(target=wait_Pusher,args='4')
p = threading.Thread(target=wait_Pusher,args='5')
while True:
    
    # if new_color != color.split('"')[9]:
    #     new_color = color.split('"')[9]
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
    #new_color = color["value"]
            new_color = color.split('"')[9]
            print(new_color)

            if new_color.lower() == 'red':
                fromPython('r')
                # wait_Pusher('0')
                r.run()
            elif new_color.lower() == 'blue':
                # fromPython('b')
                b.run()
            elif new_color.lower() == 'green':
                # fromPython('g')
                g.run()
            elif new_color.lower() == 'yello':
                # fromPython('y')
                y.run()
            elif new_color.lower() == 'purple':
                # fromPython('p')
                p.run()

sim.simxGetPingTime(clientID)
sim.simxFinish(clientID)
