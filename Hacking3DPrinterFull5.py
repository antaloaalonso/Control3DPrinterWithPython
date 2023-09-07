from ultralytics import YOLO # Import YOLO for image recognition
import cv2 # Import OpenCV, also for image recognition
import time
import serial # Import serial for establishing connection with the printer
from pygame import mixer # Import mixer for making sounds
import pygame
mixer.init()




ser=serial.Serial("/dev/tty.usbserial-2120", 115200) # Establish connection with printer; change serial port ID if necessary
ser.write(str.encode("M84 X Y Z S12000\r\n")) # Keep motors engaged
ser.write(str.encode("M92 X160 Y160 Z800\r\n")) # Keep motors engaged
ser.write(str.encode("G28\r\n")) # Home device
ser.write(str.encode("G1 Z25 X70 Y80\r\n")) # Move to a reference point
ser.write(str.encode("M400\r\n")) # Pause until moves are completed
ser.write(str.encode("M118 E1 Iamready\r\n"))  # Send message
Tcat = ""
while "Iamready" not in Tcat:
    T = ser.read()  # Fixed typo here
    Tcat += T.decode()
    Tcat # Convert bytes to string
model = YOLO("yolov8m.pt") # Load trainded objet recognition model
camera = cv2.VideoCapture(0) # Connect camera
org = (50, 50) # Set features of box around objects
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
color = (255, 0, 0)
thickness = 2
pygame.mixer.Channel(2).play(pygame.mixer.Sound('zombie.mp3'))
ret, frame = camera.read() # Capture image
frame=cv2.rotate(frame,cv2.ROTATE_180)
results = model.predict(frame, conf=0.5) # Identify object in picture
result=results[0]
nuelements=len(result.boxes)
cordscat=[]
class_idat=[]
confcat=[]
diferencia=100
for box in result.boxes: # Identify objects in image, get coordinates and sort them from left to right
    class_id = result.names[box.cls[0].item()] # Name of the object
    cords = box.xyxy[0].tolist()
    cords = [round(x) for x in cords]       
    conf = round(box.conf[0].item(), 2) # Confidence in the prediction
    img = cv2.rectangle(frame, (cords[0], cords[1]), (cords[2], cords[3]), (0, 255, 0), 3)
    img=cv2.putText(img,"Zombie",(cords[0],cords[1]), font, fontScale, color, thickness, cv2.LINE_AA)
    cv2.imshow('face_detect', img)
    print(cords)
    print(conf)
    if class_id=="person" and conf>0.5: 
        cordscat.append(cords)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
cordscat.sort()
print(cordscat)
print("original")

for x in range (len(cordscat)): # Gets the laser to the center of the objects and fires laser
    pasos=(((cordscat[x][2]-cordscat[x][0])/2)+cordscat[x][0]-690)/10
    pasos1=-pasos
    ser.write(str.encode("G91\r\n"))   
    orden="G1 "+"X"+str(pasos1)+"F5000\r\n"
    print(orden)
    ser.write(str.encode(orden)) 	
    ser.write(str.encode("M400\r\n"))
    ser.write(str.encode("M118 E1 Iamready\r\n"))  # Home device
    Tcat = ""
    while "Iamready" not in Tcat:
        T = ser.read()  # Fixed typo here
        Tcat += T.decode()
        Tcat # Convert bytes to string
    while abs(pasos1)>1:
        ret, frame = camera.read()
        frame=cv2.rotate(frame,cv2.ROTATE_180)
        results = model.predict(frame, conf=0.5) # Identify object in picture
        result=results[0]
        nuelements=len(result.boxes)
        cordscat1=[]    
        for box in result.boxes: # Identify objects in image, get new coordinates
            class_id = result.names[box.cls[0].item()] # Name of the object
            cords = box.xyxy[0].tolist()
            cords = [round(x) for x in cords]       
            conf = round(box.conf[0].item(), 2) # Confidence in the prediction
            img = cv2.rectangle(frame, (cords[0], cords[1]), (cords[2], cords[3]), (0, 255, 0), 3)
            img=cv2.putText(img,"Zombie",(cords[0],cords[1]), font, fontScale, color, thickness, cv2.LINE_AA)
            cv2.imshow('face_detect', img)
            print(cords)
            print(conf)
            if class_id=="person" and conf>0.5: 
                cordscat1.append(cords)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        cordscat1.sort()
        print(cordscat1)
        print("pases")
        pasos=(((cordscat1[x][2]-cordscat1[x][0])/2)+cordscat1[x][0]-690)/10 # Calculate new distance
        pasos1=-pasos
        ser.write(str.encode("G91\r\n"))   
        orden="G1 "+"X"+str(pasos1)+"F5000\r\n"
        print(orden)
        ser.write(str.encode(orden)) 	
        ser.write(str.encode("M400\r\n"))
        ser.write(str.encode("M118 E1 Iamready\r\n"))
        Tcat = ""
        while "Iamready" not in Tcat:
            T = ser.read()  # Fixed typo here
            Tcat += T.decode()
    print (x)
    tiempo=0.5  
    tiempo1=0.3
    orden="G1 "+"X"+str(3)+"F5000\r\n"
    ser.write(str.encode(orden))
    time.sleep(tiempo)
    ser.write(str.encode("M107\r\n")) # Turn off laser
    ser.write(str.encode("M106\r\n")) # Turn on laser
    time.sleep(tiempo1)
    ser.write(str.encode("M107\r\n")) # Turn off laser
    pygame.mixer.Channel(1).play(pygame.mixer.Sound('blaster-2-81267.mp3'))
    time.sleep(0.1)
    pygame.mixer.Channel(3).play(pygame.mixer.Sound('pain.mp3'))
    ser.write(str.encode("M400\r\n"))
    ser.write(str.encode("M118 E1 Iamready\r\n"))
    time.sleep(tiempo)
    Tcat = ""
    while "Iamready" not in Tcat:
        T = ser.read()  # Fixed typo here
        Tcat += T.decode()
    
    ser.write(str.encode("M106\r\n")) # Turn on laser

    pygame.mixer.Channel(4).play(pygame.mixer.Sound('longlaser.mp3'))
    pygame.mixer.Channel(5).play(pygame.mixer.Sound('longscream.mp3'))
    orden="G1 "+"X"+str(-4)+"F250\r\n"
    ser.write(str.encode(orden))
    orden="G1 "+"Z"+str(-4)+"X"+str(5)+"F250\r\n"
    ser.write(str.encode(orden))
    orden="G1 "+"Z"+str(0)+"X"+str(-4)+"F250\r\n"
    ser.write(str.encode(orden))
    ser.write(str.encode("M107\r\n")) # Turn off laser
    time.sleep(4)
    pygame.mixer.Channel(4).play(pygame.mixer.Sound('blank.mp3'))
    pygame.mixer.Channel(5).play(pygame.mixer.Sound('blank.mp3'))
    orden="G1 "+"Z"+str(4)+"F5000\r\n"
    ser.write(str.encode(orden)) 	
    ret, frame1 = camera.read()
    frame1=cv2.rotate(frame1,cv2.ROTATE_180)
    cv2.imshow('face_detect', frame1)
    ser.write(str.encode("M118 E1 Iamready\r\n")) 
    time.sleep(tiempo)
    Tcat = ""
    while "Iamready" not in Tcat:
        T = ser.read()  # Fixed typo here
        Tcat += T.decode()
        Tcat # Convert bytes to string

    ser.write(str.encode("M400\r\n"))
    ser.write(str.encode("M118 E1 Iamready\r\n")) 
    time.sleep(tiempo)
    Tcat = ""
    while "Iamready" not in Tcat:
        T = ser.read()  # Fixed typo here
        Tcat += T.decode()
        Tcat# Convert bytes to string
    ser.write(str.encode("M107\r\n")) 
    ser.write(str.encode("G90\r\n"))     
    ser.write(str.encode("G1 Z25 X70 Y80\r\n"))
    ser.write(str.encode("M400\r\n"))
    ser.write(str.encode("M118 E1 Iamready\r\n"))
    Tcat = ""
    while "Iamready" not in Tcat:
        T = ser.read()  # Fixed typo here
        Tcat += T.decode()
        Tcat# Convert bytes to string
    ser.write(str.encode("G91\r\n"))
     
camera.release()
cv2.destroyWindow('face_detect')