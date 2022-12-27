import cv2
import torch
import time
import numpy as np
from vidgear.gears import CamGear
from tracker import*
points=[]
def POINTS(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :  
        colorsBGR = [x, y]
        print(colorsBGR)
        

cv2.namedWindow('FRAME')
cv2.setMouseCallback('FRAME', POINTS)            
    
           


model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

cap=cv2.VideoCapture('parking.mp4')
count=0




while True:
    ret,frame=cap.read()
    if not ret:
        break
#    frame = stream.read()
#    count += 1
#    if count % 2 != 0:
#        continue
    frame=cv2.resize(frame,(1020,600))
#    h,w,_=frame.shape
#    print(w)

    results=model(frame)

#    frame=np.squeeze(results.render())
    list=[]
    for index, row in results.pandas().xyxy[0].iterrows():
        x1 = int(row['xmin'])
        y1 = int(row['ymin'])
        x2 = int(row['xmax'])
        y2 = int(row['ymax'])
        d=(row['name'])
        cx=int(x1+x2)//2
        cy=int(y1+y2)//2
        if 'car' in d:
           cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),3)
           cv2.putText(frame,str(d),(x1,y1),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),2)

    cv2.imshow("FRAME",frame)
    cv2.setMouseCallback("FRAME",POINTS)
   
    time.sleep(1)
    if cv2.waitKey(1)&0xFF==27:
        break
cap.release()
cv2.destroyAllWindows()

