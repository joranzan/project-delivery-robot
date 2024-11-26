from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
from Raspi_PWM_Servo_Driver import PWM
from time import sleep
import paho.mqtt.client as mqtt
import threading
import BROKER.broker_address as broker_address

mh = Raspi_MotorHAT(addr=0x6f) 
myMotor = mh.getMotor(2) #핀번호

servo = PWM(0x6F)
servo.setPWMFreq(60)  # Set frequency to 60 Hz

curAngle = 350
step = 30
curSpeed = 0
accel = 50

def on_message(client, userdata, message):
    command = str(message.payload.decode("utf-8")) 
    if command == '1':
        GO()
    if command == '2':
        LEFT()
    if command == '3':
        RIGHT()
    if command == '4':
        BACK()
    if command == '5':
        STOP()
    if command == '6':
        #MIDDLE()
        mqttc2.publish("params/buzzer", 200)
    mqttc2.publish("gear", curSpeed/50)

def GO():
    global curSpeed
    curSpeed += accel
    if curSpeed > 250:
        curSpeed = 250
	#myMotor.setSpeed(200)
    if curSpeed < 0:
        myMotor.setSpeed(-1*curSpeed)
        myMotor.run(Raspi_MotorHAT.BACKWARD)
    else:
        myMotor.setSpeed(curSpeed)
        myMotor.run(Raspi_MotorHAT.FORWARD)
    #print("go")
    
def LEFT():
    global curAngle
    curAngle = curAngle - step
    if curAngle<230:
        curAngle = 230
    elif curAngle>=335 and curAngle<=355:
        curAngle = 345
    servo.setPWM(0, 0, curAngle)
    #print("left")

def RIGHT():
    global curAngle
    curAngle = curAngle + step
    if curAngle >430:
        curAngle = 430
    elif curAngle>=335 and curAngle<=355:
        curAngle = 345
    servo.setPWM(0, 0, curAngle)
    #print("right")

def BACK():
    global curSpeed
    curSpeed -= accel
    if curSpeed < -250:
        curSpeed = -250
	#myMotor.setSpeed(100)
    if curSpeed < 0:
        myMotor.setSpeed(-1*curSpeed)
        myMotor.run(Raspi_MotorHAT.BACKWARD)
    else:
        myMotor.setSpeed(curSpeed)
        myMotor.run(Raspi_MotorHAT.FORWARD)
    #print("back")

def STOP():
    global curAngle
    global curSpeed
    curAngle = 350
    curSpeed = 0
    myMotor.run(Raspi_MotorHAT.RELEASE)
    servo.setPWM(0, 0, 350)
    #print("stop")

def MIDDLE():
	servo.setPWM(0, 0, 345)
	#print("middle")
    
try:
    mqttc2 = mqtt.Client("python_pub2")
    mqttc2.connect(broker_address, 1883)
    mqttc2.publish("gear", 0)
    client1 = mqtt.Client("client1")
    client1.connect(broker_address)
    client1.subscribe("car")
    client1.on_message = on_message
    client1.loop_forever() 

finally:
    myMotor.run(Raspi_MotorHAT.RELEASE)
    	
    #print("go")

