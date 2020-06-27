import gpiozero, time, Rider, configparser, flask, multiprocessing
from enum import Enum
from Rider import Rider

class Mode(Enum):
    disabled = 1
    idle = 2
    running = 3
    quitting = 4

class Slide:
    rider = Rider()
    status = Mode

    def load_configuration(self, configuration):
        config = configparser.ConfigParser()
        config.read(configuration)

        self.distance = int(config["DEFAULT"]["distance"])

        self.GREEN_LED = gpiozero.LED(int(config["GPIO"]["light_green"]), active_high = False, initial_value=True)
        self.RED_LED = gpiozero.LED(int(config["GPIO"]["light_red"]), active_high = False)

        self.TOP = gpiozero.Button(int(config["GPIO"]["sensor_top"]), pull_up=True, active_state=None)
        self.BOTTOM = gpiozero.Button(int(config["GPIO"]["sensor_bottom"]), pull_up=True, active_state=None)

        self.MAX_TIME = int(config["TIMING"]["auto_reset_time"])
        self.MIN_TIME = int(config["TIMING"]["ignore_time"])

        self.route_status = "/slide/" + config["DEFAULT"]["name"] + "/status"
        self.name = config["DEFAULT"]["name"]
        print("loaded configuration: " + self.name)
        return

    def configure_server(self, api):
        self.api = api
        api.add_url_rule(self.route_status, self.route_status ,self.request_status, methods=["POST"])

    def __init__(self, api, configuration=None):
        # TODO: load highscores

        # configuration
        self.load_configuration(configuration)
        self.configure_server(api)
        self.start()
        return


    def interupt_sensor_top(self):
        if(self.status == Mode.running):
            return
        print("interupt_sensor_top")
        
        self.status = Mode.running
        self.rider.start_time()
        self.GREEN_LED.off()
        self.RED_LED.on()

    def interupt_sensor_bottom(self):
        if(self.status == Mode.idle):
            return
        if(self.rider.get_time() < self.MIN_TIME):
            return
        print("interupt_sensor_bottom")

        print("Time: " + str(round(self.rider.get_time(),2)) + "s")
        print("Speed: " + str(round(self.rider.get_speed(self.distance),2)) + "m/s")

        self.status = Mode.idle
        self.GREEN_LED.on()
        self.RED_LED.off()

    def interupt_soft_reset(self):
        print("interupt_soft_reset")
        self.status = Mode.idle
        self.GREEN_LED.on()
        self.RED_LED.off()

    def request_status(self):
        print("request_status")
        return str(self.status)
    
    def start(self):
        print("start")
        self.TOP.when_pressed = self.interupt_sensor_top
        self.BOTTOM.when_pressed = self.interupt_sensor_bottom

        self.status = Mode.idle
        self.GREEN_LED.on()

        while(True):
            if (self.status == Mode.running) and (self.rider.get_time() > self.MAX_TIME):
                self.interupt_soft_reset()
            time.sleep(1)

        return