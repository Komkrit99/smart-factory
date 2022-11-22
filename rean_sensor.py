import sim
import json
from time import sleep
import urllib3
import threading
http    = urllib3.PoolManager()
print ("Program started")
sim.simxFinish(-1)
clientID = sim.simxStart('127.0.0.1',19997,True,True,5000,5)
def connect():
    if clientID!=-1:
        print ("Connected")
        sim.simxAddStatusbarMessage(clientID,'Hello CoppeliaSim!',sim.simx_opmode_oneshot)
    else:
        print ("Not Connected")
def fromPython(msg):
    print(msg)
    inputInts=[]
    inputFloats=[]
    inputStrings=msg
    inputBuffer=bytearray()
    res,retInts,retFloats,retStrings,retBuffer=sim.simxCallScriptFunction(clientID,'ConveyorBelt'
    ,sim.sim_scripttype_childscript,'fromPython',inputInts,inputFloats,inputStrings,inputBuffer,sim.simx_opmode_blocking)
    sim.simxAddStatusbarMessage(clientID,'finish!',sim.simx_opmode_oneshot)
    print('sented')
def pusher(number):
    for t in range(3):
    # Activate
        data_json   = {"action" : 1}
        data_encode = json.dumps(data_json).encode("utf-8")
        res = http.request("POST",
                            "http://localhost/tss/0/actuator/"+number,
                            body=data_encode,
                            headers={"Content-Type" : "application/json"}) 
        text    = res.data.decode("utf-8")
        print(text)
        sleep(1)
        # Deactivate
        data_json   = {"action" : 0}
        data_encode = json.dumps(data_json).encode("utf-8")
        res = http.request("POST",
                            "http://localhost/tss/0/actuator/"+number,
                            body=data_encode,
                            headers={"Content-Type" : "application/json"})
        text    = res.data.decode("utf-8")
        print(text)
        sleep(1)
def wait_Pusher(number):
    while True:
        res = http.request( "GET",
                            "http://localhost/tss/0/sensor/"+number
                            )
        num    = res.data.decode("utf-8")
        num.split('"')[9]
        # if num.split('"')[9] == '1':
        #     threading.Thread(target=pusher ,args=num.split('"')[9])
            # pusher(number)
            #break
new_color = ''         
while True:
    res = http.request( "GET",
                        "http://localhost/tss/0/sensor/8"
                        )
    color    = res.data.decode("utf-8")
    if new_color != color[43]:
        new_color = color[43]
        print(new_color)
    
    # #new_color = color["value"]
    #     print(new_color)
        
        # if new_color.lower() == 'red':
        #     fromPython('r')
        #     # wait_Pusher('0')
        #     threading.Thread(target=wait_Pusher,args=0)
        # elif new_color.lower() == 'blue':
        #     fromPython('b')
        #     # threading.Thread(target=wait_Pusher,args=1)
        # elif new_color.lower() == 'green':
        #     fromPython('g')
        #     # threading.Thread(target=wait_Pusher,args=2)
        # elif new_color.lower() == 'yello':
        #     fromPython('y')
        #     # threading.Thread(target=wait_Pusher,args=3)
        # elif new_color.lower() == 'purple':
        #     fromPython('p')
            # threading.Thread(target=wait_Pusher,args=3)

sim.simxGetPingTime(clientID)
sim.simxFinish(clientID)