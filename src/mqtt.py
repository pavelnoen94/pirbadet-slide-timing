import paho.mqtt.client as mqtt
import json


class message_sender():
    def __init__(self, name, target):
        self.mqttc = mqtt.Client()
        self.name = name
        self.mqttc.connect(target)
    
    def send(self, topic, message):
        self.mqttc.publish(self.name + "/" + topic, message)
    
    def send_obj(self, topic, input_object):
        self.mqttc.publish(self.name + "/" + topic, json.dumps(input_object, indent=4, sort_keys=True, default=str))

    def loop_start(self):
        self.mqttc.loop_start()

    def loop_stop(self):
        self.mqttc.loop_stop()
    
    def subscribe(self, topic):
        self.mqttc.subscribe(self.name + "/" + topic)
    
    def message_callback_add(self, topic, callback):
        self.mqttc.message_callback_add(self.name + "/" + topic, callback)
