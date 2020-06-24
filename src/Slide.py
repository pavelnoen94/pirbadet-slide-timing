import gpiozero, time, Rider, highscores, configparser, flask
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

        self.GREEN = gpiozero.LED(int(config["GPIO"]["light_green"]))
        self.RED = gpiozero.LED(int(config["GPIO"]["light_red"]))

        self.TOP = gpiozero.Button(int(config["GPIO"]["sensor_top"]), pull_up=False)
        self.BOTTOM = gpiozero.Button(int(config["GPIO"]["sensor_bottom"]), pull_up=False)

        self.MAX_TIME = int(config["TIMING"]["auto_reset_time"])
        self.MIN_TIME = int(config["TIMING"]["ignore_time"])

        self.route_status = "/" + config["DEFAULT"]["name"] + "/status"
        self.route_enable = "/" + config["DEFAULT"]["name"] + "/enable"
        self.route_disable = "/" + config["DEFAULT"]["name"] + "/disable"

        print("loaded configuration: " + config["DEFAULT"]["name"])
        return


    def __init__(self, api, configuration=None):
        # TODO: signal interupt handler
        # TODO: load highscores

        self.load_configuration(configuration)
        print(self.route_enable)
        self.configure_server(api)

        self.start()
        return

    def configure_server(self, api):
        self.api = api
        api.add_url_rule(self.route_status, self.route_status ,self.request_status)
        api.add_url_rule(self.route_enable, self.route_enable ,self.request_enable)
        api.add_url_rule(self.route_disable, self.route_disable ,self.request_disable)

    def mode_selector(self):
        if(self.status == Mode.disabled):
            self.disabled()
            return
        self.status = Mode.idle

    def start(self):
        self.mode_picker()


    def mode_picker(self):
        print("mode picker")
        while (True):
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
        print("disabled")

        # turn off lights
        self.GREEN.off()
        self.RED.off()
        # wait for enable switch
        while (self.status == Mode.disabled):
            pass

        print("enabled")
        self.status = Mode.idle
        return


    def idle(self):
        print("idle")

        # Green light!
        self.RED.off()
        self.GREEN.on()

        # wait for a rider
        while (not self.TOP.is_pressed):
            # return if interupted by reset or disable
            if (self.status != Mode.idle):
                return

        # Red light! Start timer
        self.rider.start_time()
        self.RED.on()
        self.GREEN.off()

        self.status = Mode.running
        return


    def running(self):
        print("running")

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
                print("auto reset")            
        else:
            # print time and speed
            currentTime = self.rider.get_time()
            print("time: " + str(round(currentTime,2)) + "s")
            currentSpeed = self.rider.get_speed(self.distance)
            print("speed: " + str(round(currentSpeed,2)) + "m/s")

        self.status = Mode.idle

        return

    # reset timers and stuff
    def soft_reset(self):
        print("soft reset")

        # set disabled to quit all states and restart
        self.status = Mode.disabled
        self.RED.off()
        self.GREEN.off()
        return

    # spawn a cloned process
    def hard_reset(self):
        print("hard reset")
        self.soft_reset() # temp solution
        # TODO: restart self
        return

    def request_status(self):
        return str(self.status)

    def request_enable(self):
        self.status = Mode.idle
        return "ok"

    def request_disable(self):
        self.status = Mode.disabled
        return "ok"