# import paho.mqtt.client as mqtt
#
# # subscriber callback
# def on_message(client, userdata, message):
#     print("message received ", str(message.payload.decode("utf-8")))
#     print("message topic=", message.topic)
#     print("message qos=", message.qos)
#     print("message retain flag=", message.retain)
#
#
# broker_address = "127.0.0.1"
# #구독자 이름
# client1 = mqtt.Client("client1")
# #broker 주소 등록
# client1.connect('localhost', 1883)
# #등록하고픈 토픽 지정
# client1.subscribe("camera/data")
# client1.on_message = on_message
# client1.loop_forever()
#
#

import base64
from datetime import datetime
import paho.mqtt.client as mqtt
import cv2
import numpy as np

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)

def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))

def on_subscribe(client, userdata, mid, granted_qos):
    print("subscribed: " + str(mid) + " " + str(granted_qos))

def create_figure(header):
    print("create figure with ",header)
first_msg = 0
im = 0
def on_message(client, userdata, msg):
    print("[" + datetime.today().strftime("%Y/%m/%d %H:%M:%S") + "] topic : " + msg.topic)
    img = base64.b64decode(msg.payload)
    # converting into numpy array from buffer
    npimg = np.frombuffer(img, dtype=np.uint8)
    # Decode to Original Frame
    frame = cv2.imdecode(npimg, 1)
    cv2.imshow("01img",frame)
    cv2.waitKey(1)

# 새로운 클라이언트 생성
client = mqtt.Client()
client.username_pw_set(username='james',password='james12!')
# 콜백 함수 설정 on_connect(브로커에 접속), on_disconnect(브로커에 접속종료), on_subscribe(topic 구독), on_message(발행된 메세지가 들어왔을 때)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_subscribe = on_subscribe
client.on_message = on_message

client.connect('10.196.72.113', 1883)
client.subscribe('sensors/test/#', 1)
client.loop_forever()

# client.loop_start()
# while True:
#     cv2.imshow("Stream", frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
 
# # Stop the Thread
# client.loop_stop()

# import base64
# import cv2
# import numpy as np
# import paho.mqtt.client as mqtt
# import time,os
 
# MQTT_BROKER = "10.196.72.113"
# MQTT_TOPIC = "sensors/test/#"
# BASEDIR = os.path.dirname(__file__)
 
 
# frame = np.zeros((480, 640, 3), np.uint8)
 
# # The callback for when the client receives a CONNACK response from the server.
# def on_connect(client, userdata, flags, rc):
#     print("Connected with result code "+str(rc))
#     # Subscribing in on_connect() means that if we lose the connection and
#     # reconnect then subscriptions will be renewed.
 
# # The callback for when a PUBLISH message is received from the server.
# def on_message(client, userdata, msg):
#     global frame, captureFolder
#     # Decoding the message
#     img = base64.b64decode(msg.payload)
#     # converting into numpy array from buffer
#     npimg = np.frombuffer(img, dtype=np.uint8)
#     # Decode to Original Frame
#     frame = cv2.imdecode(npimg, 1)
#     now = int(time.time())
#     filesFolder = os.path.join(captureFolder,f'{now}.jpg')
#     cv2.imwrite(filesFolder,frame)
#     print("write")
 
# # def checkfolder():
# #     folder = os.path.join(BASEDIR,MQTT_TOPIC)
# #     if not os.path.exists(folder):
# #         print(f'{MQTT_TOPIC} Folder was Created!')
# #         os.mkdir(folder)
# #     return folder
 
# # captureFolder = checkfolder()
# # print(captureFolder)
# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message
# client.connect(MQTT_BROKER)
# client.subscribe(MQTT_TOPIC,1)
# # Starting thread which will receive the frames
# client.loop_start()
 
# while True:
#     cv2.imshow("Stream", frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
 
# # Stop the Thread
# client.loop_stop()