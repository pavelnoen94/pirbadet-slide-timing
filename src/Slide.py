import gpiozero, time, Rider, highscores, configparser, flask, signal, sys
from enum import Enum
from Rider import Rider
from relay_lib_seed import *

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

        self.GREEN_LED = gpiozero.LED(int(config["GPIO"]["light_green"]))
        self.RED_LED = gpiozero.LED(int(config["GPIO"]["light_red"]))
        self.GREEN_RELAY = int(config["RELAY"]["light_green"])
        self.RED_RELAY = int(config["RELAY"]["light_red"])

        self.TOP = gpiozero.Button(int(config["GPIO"]["sensor_top"]), pull_up=False)
        self.BOTTOM = gpiozero.Button(int(config["GPIO"]["sensor_bottom"]), pull_up=False)

        self.MAX_TIME = int(config["TIMING"]["auto_reset_time"])
        self.MIN_TIME = int(config["TIMING"]["ignore_time"])

        self.route_status = "/slide/" + config["DEFAULT"]["name"] + "/status"
        self.route_enable = "/slide/" + config["DEFAULT"]["name"] + "/enable"
        self.route_disable = "/slide/" + config["DEFAULT"]["name"] + "/disable"
        self.route_reset = "/slide/" + config["DEFAULT"]["name"] + "/reset"
        self.name = config["DEFAULT"]["name"]
        print("loaded configuration: " + self.name)
        return

    def __init__(self, api, configuration=None):
        # TODO: load highscores

        # configuration
        self.load_configuration(configuration)
        self.configure_server(api)

        self.start()
        return

    def configure_server(self, api):
        self.api = api
        api.add_url_rule(self.route_status, self.route_status ,self.request_status, methods=["POST"])
        api.add_url_rule(self.route_enable, self.route_enable ,self.request_enable, methods=["POST"])
        api.add_url_rule(self.route_disable, self.route_disable ,self.request_disable, methods=["POST"])
        api.add_url_rule(self.route_reset, self.route_reset ,self.request_reset, methods=["POST"])

    def mode_selector(self):
        if(self.status == Mode.disabled):
            self.disabled()
            return
        self.status = Mode.idle

    def start(self):
        self.mode_picker()


    def mode_picker(self):
        while (True):
            print("[" + self.name + "] mode picker")
            self.mode_selector()
            if(self.status == Mode.idle):
                self.idle()
            if(self.status == Mode.running):
                self.running()
            if(self.status == Mode.disabled):
                self.disabled()
            if(self.status == Mode.quitting):
                # TODO: close all open files, save configurations
                return
        return


    def disabled(self):
        print("[" + self.name + "] disabled")

        # turn off lights
        self.GREEN_LED.off()
        self.RED_LED.off()

        relay_lib_seed.relay_off(self.GREEN_RELAY)
        relay_lib_seed.relay_off(self.RED_RELAY)

        # wait for enable switch
        while (self.status == Mode.disabled):
            pass

        print("[" + self.name + "] enabled")
        self.status = Mode.idle
        return


    def idle(self):
        print("[" + self.name + "] idle")

        # Green light!
        self.RED_LED.off()
        self.GREEN_LED.on()

        relay_lib_seed.relay_off(self.RED_RELAY)
        relay_lib_seed.relay_on(self.GREEN_RELAY)


        # wait for a rider
        while (not self.TOP.is_pressed):
            # return if interupted by reset or disable
            if (self.status != Mode.idle):
                return

        # Red light! Start timer
        self.rider.start_time()
        self.RED_LED.on()
        self.GREEN_LED.off()
        relay_lib_seed.relay_off(self.GREEN_RELAY)
        relay_lib_seed.relay_on(self.RED_RELAY)

        self.status = Mode.running
        return


    def running(self):
        print("[" + self.name + "] running")

        # ignore top input for minimum time
        while (self.rider.get_time() < self.MIN_TIME):
            # return if interupted by reset or disable
            if (self.status != Mode.running):
                return

        # wait for a user to exit the track.
        while (not self.BOTTOM.is_pressed):
            if (self.status != Mode.running):
                return
            if (self.rider.get_time() > self.MAX_TIME):
                break

        if (self.rider.get_time() > self.MAX_TIME):
                print("[" + self.name + "] auto reset")
        else:
            # print time and speed
            currentTime = self.rider.get_time()
            print("[" + self.name + "] time: " + str(round(currentTime,2)) + "s")
            currentSpeed = self.rider.get_speed(self.distance)
            print("[" + self.name + "] speed: " + str(round(currentSpeed,2)) + "m/s")

        self.status = Mode.idle

        return

    # reset timers and stuff
    def soft_reset(self):
        print("[" + self.name + "] soft reset")

        # set disabled to quit all states and restart
        self.status = Mode.idle
        self.RED_LED.off()
        self.GREEN_LED.off()

        relay_lib_seed.relay_off(self.GREEN_RELAY)
        relay_lib_seed.relay_off(self.RED_RELAY)

        return

    # spawn a cloned process
    def hard_reset(self):
        print("[" + self.name + "] hard reset")
        self.soft_reset() # temp solution
        # TODO: restart self
        return

    def request_status(self):
        return str(self.status)

    def request_enable(self):
        self.status = Mode.idle
        return str(self.status)

    def request_disable(self):
        self.status = Mode.disabled
        return str(self.status)

    def request_reset(self):
        self.soft_reset()
        return str(self.status)