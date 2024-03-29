import sys
from math import *
import numpy as np
import socket
import time
import paho.mqtt.client as mqtt

IP_ADDRESS = '192.168.0.212'
clientAddress = "192.168.0.25"
MQTTHOST = "192.168.0.36"
MQTTPORT = 1883
MQTTTOPIC = "blob"
mqttClient = mqtt.Client()

# Connect to the robot
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP_ADDRESS, 5000))
print('Connected')

def Left_Turn():
    command = 'CMD_MOTOR#-1300#-1300#1500#1500\n'
    s.send(command.encode('utf-8'))
    
def Right_Turn():
    command = 'CMD_MOTOR#1500#1500#-1300#-1300\n'
    s.send(command.encode('utf-8'))

def Terminate():
    command = 'CMD_MOTOR#00#00#00#00\n'
    s.send(command.encode('utf-8'))

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    mqttClient.subscribe(MQTTTOPIC)

def on_message(client, userdata, msg):
    ball = str(msg.payload.decode("utf-8"))
    val = [eval(i) for i in ball.split(' ')]
    Orien(val[0], val[1])

def Orien(center, size):
    if size > 2500:
        Terminate()
        time.sleep(10)
    # print("Center", center)
    w = 15 * center
    v = 0.4 * (2500 - size)
    u = np.array([v-w, v+w])
    print("u: ", u[0], u[1])
    u[u > 1000.] = 1000.
    u[u < -1000.] = -1000.
    print("u actual: ", u[0], u[1])
    command = 'CMD_MOTOR#%d#%d#%d#%d\n'%(u[0], u[0], u[1], u[1])
    s.send(command.encode('utf-8'))
    # print(command)
    # time.sleep(0.1)
    # Terminate()

start = time.time()

if __name__ == '__main__':
    try:
        mqttClient.on_connect = on_connect
        mqttClient.on_message = on_message
        mqttClient.connect("test.mosquitto.org", MQTTPORT)
        mqttClient.loop_start()
        while ((time.time() - start) < 60):
            pass
        mqttClient.loop_stop()
    except KeyboardInterrupt:
        Terminate()
        sys.exit(0)

print("Done")
# Close the connection
s.shutdown(2)
s.close()