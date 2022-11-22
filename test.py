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


def pusher(number,ping):
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
    num_count = 0
    res = http.request( "GET",
                        "http://localhost/tss/0/latency"
                        )
    pings    = res.data.decode("utf-8")
    # if new_color != color[43]:
    #     new_color = color[43]
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
        #     threading.Thread(target=pusher ,args=num.split('"')[9])
            if num_count == 2:
                break
    print('breal')
    pusher(number,0)



new_color = ''
new_sensor_0 = ''
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
                threading.Thread(target=wait_Pusher,args='1').start()
            elif new_color.lower() == 'blue':
                # fromPython('b')
                threading.Thread(target=wait_Pusher,args='2').start()
            elif new_color.lower() == 'green':
                # fromPython('g')
                threading.Thread(target=wait_Pusher,args='3').start()
            elif new_color.lower() == 'yellow':
                # fromPython('y')
                threading.Thread(target=wait_Pusher,args='4').start()
            elif new_color.lower() == 'purple':
                # fromPython('p')
                threading.Thread(target=wait_Pusher,args='5').start()

sim.simxGetPingTime(clientID)
sim.simxFinish(clientID)
