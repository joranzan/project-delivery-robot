import paho.mqtt.client as mqtt
from gpiozero import DistanceSensor, TonalBuzzer
from time import sleep
import BROKER.broker_address as broker_address


sensor1 = DistanceSensor(echo=15, trigger=14)
sensor2 = DistanceSensor(echo=24, trigger=23)
sensor3 = DistanceSensor(echo=19, trigger=26)

def sensing():
    mqttc = mqtt.Client("python_pub")
    mqttc.connect(broker_address, 1883)

    while True:
        #print(sensor1.distance, end=" // ")
        #print(sensor2.distance)
        mqttc.publish("params/sensor1", round(sensor1.distance*100,2))
        mqttc.publish("params/sensor2", round(sensor2.distance*100,2))
        mqttc.publish("params/sensor3", round(sensor3.distance*100,2))
        sleep(0.2)

sensing()
