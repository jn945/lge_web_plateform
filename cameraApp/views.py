from django.shortcuts import render
from django.http import JsonResponse
import paho.mqtt.client as mqtt
import threading
import time,sys, cv2
from datetime import datetime
# Create your views here.

def index(request):
    print("debub >>>>>  localhost:8000/james/index/ >>> index func")
    return render(request,'james/camera.html')

def ajax(request):
    print("Debug >>>>>>>> localhost:8000/james/ajax >> camera ajax")
    datalist = [0,10,20,30,40,40,20,20,10,70]
    context = {'datalist':datalist}
    return JsonResponse(context, safe=False) # safe=False가 비동기다

MQTT_TOPIC = "Video_Group_Camera"
def mqtt_subscribe(request):
    # def on_connect(client, userdata, flags, rc):
    #     print("Connected with result code "+str(rc))
    #     client.subscribe("Video_Group_Camera")

    # def on_message(client, userdata, msg):
    #     # print(msg.topic+" "+str(msg.payload))
    #     print("msg.topic"+"on Message")
    #     response = {'img': msg.payload.decode()}
    #     client.disconnect()
    #     return JsonResponse(response, safe=False)

    # client = mqtt.Client()
    # client.on_connect = on_connect
    # client.on_message = on_message
    # client.username_pw_set(username='james',
    #                        password='james12!')
    # # client.connect("10.196.72.113", 1883, 60)
    # client.connect("localhost", 1883, 60)

    # print(id(client))
    # client.loop_start()
    # time.sleep(5)
    # client.loop_stop()

    client= MQTTCamera(MQTT_TOPIC)
    threading.Thread(target=mqttloop,args=(client,True))
    # client.mqttloop()
def mqttloop(obj,que):
    obj.mqttloop(que)

class MQTTCamera:
    def __init__(self,topic):
        # self.cap , self.camera_size = self.get_cap_object()
        self.client = mqtt.Client("mydesk")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        # self.client.on_publish = self.on_publish
        self.client.username_pw_set(username="james",password="james12!")
        self.client.connect("10.196.72.113",1883, 60)
        # self.client.connect("localhost",1883, 60)
    
    def on_message(self,client, userdata, msg):
        print("[" + datetime.today().strftime("%Y/%m/%d %H:%M:%S") + "] topic : " + msg.topic)
        # print("payload : " + str(msg.payload))
        response = {'img': msg.payload.decode()}
        self.client.loop_stop()
        self.client.disconnect()
        return JsonResponse(response, safe=False)
    
    def subs_image(self):
        self.client.subscribe("Video_Group_Camera")
        self.client.loop_start()
   
    def get_cap_object(self):
        cap = cv2.VideoCapture(0+cv2.CAP_DSHOW)
        assert cap.isOpened() , "Can't connect Camera, Make sure connection"

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return cap, (width, height)
    
    def cap_image(self):
        ret, frame = self.cap.read()
        if ret == False:
            frame = self.get_random_numpy(self.camera_size)

        frame = self.addInfo_img(frame)
        frame_Bytearr = self.imgToByte(frame)
        self.client.publish(MQTT_TOPIC,frame_Bytearr)

        # client.publish("sensor/test/time",frame_Bytearr)
        # cv2.imshow("img",frame)
        # cv2.waitKey(1)
        currtime = time.time()
        time.sleep(2)
    
    def addInfo_img(self,frame):
        currTime = self.read_time()
        cv2.rectangle(frame,(0,5),(360,40),(255,255,255),-1)
        cv2.putText(frame,currTime,
                    (0,30),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1,
                    color=(0,0,0),
                    thickness=1,
                    lineType=2
                    )
        return frame
    
    def imgToByte(self,frame):
        import base64
        imgByteArr = cv2.imencode('.png', frame)[1].tobytes()
        jpg_as_text = base64.b64encode(imgByteArr)
        return jpg_as_text
        '''
        case1. using cv2.imencode()[1].tostring()
        case2. using base64.b64encode(cv2.imencode()[1])
        '''
        # return imgByteArr
    def get_random_numpy(self,size:tuple):
        """Return a dummy frame."""
        return np.random.randint(0, 100, size=(size[1], size[0]),dtype=np.uint8)

    def read_time(self):
        return datetime.today().strftime("%Y/%m/%d %H:%M:%S")

    # def on_publish(self,client, userdata, mid):
    #     print("[" + datetime.today().strftime("%Y/%m/%d %H:%M:%S") + "] on_publish Ture >>" + MQTT_TOPIC)

    def on_connect(self,client,userdata,flags,rc): 
        print("Connected with result code "+str(rc))
        if rc == 0 :
            print("rc : " ,rc)
        else : 
            print(rc)
    
    def mqttloop(self,que:bool):
        while True:
            if not que:
                break

            try:
                # self.cap_image()
                self.subs_image()
                # read_time_org()
            except KeyboardInterrupt:
                sys.exit(0)