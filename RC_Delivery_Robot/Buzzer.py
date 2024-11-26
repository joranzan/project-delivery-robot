from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
from time import sleep
import paho.mqtt.client as mqtt
import BROKER.broker_address as broker_address


bell = TonalBuzzer(16)

def on_message(client, userdata, message):
    dt = float(message.payload.decode("utf-8"))
    if dt < 15:
        bell.play(300)
        sleep(0.1)
        bell.stop()
    elif dt == 200:
        bell.play(700)
        sleep(0.2)
        bell.stop()

client2 = mqtt.Client("client2")

def on_connect(client, userdata, flags, rc):
    client.subscribe("params/+")

client2.on_connect = on_connect
client2.on_message = on_message

client2.connect(broker_address, 1883, 60)
client2.loop_forever()

