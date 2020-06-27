import gpiozero, time, Rider, configparser, highscores, signal
from enum import Enum
from Rider import Rider


class Mode(Enum):
    disabled = 1
    idle = 2
    running = 3
    quitting = 4


class Slide:


    def __init__(self, configuration, termination_signal):
        self.termination_signal = termination_signal
        self.load_configuration(configuration)
        self.highscore = highscores.high_scores(self.name)
        self.start()

        return


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

        self.name = config["DEFAULT"]["name"]
        self.rider = Rider()
        self.status = Mode

        print("loaded configuration: " + self.name)

        return


    def interupt_sensor_top(self):
        if(self.status == Mode.running):
            return
        print("interupt_sensor_top")
        
        self.status = Mode.running
        self.rider.start_time()
        self.GREEN_LED.off()
        self.RED_LED.on()

        return


    def interupt_sensor_bottom(self):
        if(self.status == Mode.idle):
            return
        if(self.rider.get_time() < self.MIN_TIME):
            return
        print("interupt_sensor_bottom")

        print("Time: " + str(round(self.rider.get_time(),2)) + "s")
        print("Speed: " + str(round(self.rider.get_speed(self.distance),2)) + "m/s")

        self.highscore.add_time(round(self.rider.get_time(),2))
        self.status = Mode.idle
        self.GREEN_LED.on()
        self.RED_LED.off()

        return


    def interupt_soft_reset(self):
        print("interupt_soft_reset")
        self.status = Mode.idle
        self.GREEN_LED.on()
        self.RED_LED.off()

        return


    def start(self):
        print("start")
        self.TOP.when_pressed = self.interupt_sensor_top
        self.BOTTOM.when_pressed = self.interupt_sensor_bottom

        self.status = Mode.idle
        self.GREEN_LED.on()

        while not self.termination_signal.is_set():
            if (self.status == Mode.running) and (self.rider.get_time() > self.MAX_TIME):
                self.interupt_soft_reset()
            time.sleep(1)
        self.highscore.save_highscores()
        self.highscore.print_highscores()

        return

    def quit(self):
        print("quit")
        self.mode = Mode.quitting
