import threading
import time
import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
msg = 0
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
def updateapi():
    aa = ['RED','BLUE','GREEN','YELLOW','PURPLE']
    global msg
    while(True):
        msg = random.choice(aa)
        time.sleep(3)

threading.Thread(target=updateapi).start()

@app.get("/color/")
async def root():
    global msg
    return {'id':'10','type':'Color',"value": msg,}
@app.get("/wait/")
async def root2():
    return {'id0':id0,'id1':id1,'id2':id2,
    'id3':id3,'id4':id4,'id5':id5,
    'id6':id6,'id7':id7,'id8':id8,'id9':id9}
@app.get("/left/")
async def root3():
    return {'r':r_n,'b':b_n,"g": g_n,'y':y_n,'p':p_n}