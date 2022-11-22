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


def pusher(number):
    data_json = {"action": 1}
    data_encode = json.dumps(data_json).encode("utf-8")
    res = http.request("POST",
                       "http://localhost/tss/0/actuator/"+number,
                       body=data_encode,
                       headers={"Content-Type": "application/json"})
    text = res.data.decode("utf-8")
    print(text)
    sleep(1)
    #Deactivate
    data_json = {"action": 0}
    data_encode = json.dumps(data_json).encode("utf-8")
    res = http.request("POST",
                       "http://localhost/tss/0/actuator/"+number,
                       body=data_encode,
                       headers={"Content-Type": "application/json"})
    text = res.data.decode("utf-8")
    print(text)
    sleep(1)


pusher('3')
sim.simxGetPingTime(clientID)
sim.simxFinish(clientID)
