import gpiozero, time, Rider, highscores
from enum import Enum
from Rider import Rider

class Mode(Enum):
    disabled = 1
    idle = 2
    running = 3


class Slide:
    # TODO: put inside a configuration file
    MIN_TIME = 10 
    MAX_TIME = 40
    DISTANCE = 100 # assuming the slide is 100m long


    # Outputs
    GREEN = gpiozero.LED(13)             # Green trffic light
    RED = gpiozero.LED(19)               # Red traffic light
    BLUE = gpiozero.LED(26)              # Someone is riding right now (for debugging)

    # Inputs
    TOP = gpiozero.Button(24, pull_up=False)
    BOTTOM = gpiozero.Button(16, pull_up=False)
    RESET_HARD = gpiozero.Button(20, pull_up=False)          # clears current run and starts over again
    RESET_SOFT = gpiozero.Button(21, pull_up=False)          # terminate the application and restart it
    ENABLED = gpiozero.Button(6, pull_up=None, active_state=True)

    rider = Rider()
    status = Mode


    def load_configuration(self, configuration):
        # TODO: load configuration from file
        pass

        return


    def __init__(self, configuration=None):
        # enable reset button
        self.RESET_SOFT.when_pressed = self.soft_reset
        self.RESET_HARD.when_pressed = self.hard_reset
        self.ENABLED.when_released = self.disabled

        # TODO: signal interupt handler
        # TODO: load highscores

        self.load_configuration(configuration)
        return

    def mode_selector(self):
        if(not self.ENABLED.is_pressed):
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

        return


    def disabled(self):
        print("disabled")

        # turn off lights
        self.GREEN.off()
        self.RED.off()
        self.BLUE.off()
        # wait for enable switch
        while (not self.ENABLED.is_pressed):
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

        # indicate that someone is riding
        self.BLUE.on()

        # wait for a user to exit the track.
        while (not self.BOTTOM.is_pressed):
            if (self.status != Mode.running):
                return

        # print time and speed
        currentTime = self.rider.get_time()
        print("time: " + str(round(currentTime,2)) + "s")
        currentSpeed = self.rider.get_speed(self.DISTANCE)
        print("speed: " + str(round(currentSpeed,2)) + "m/s")


        self.BLUE.off()
        self.status = Mode.idle

        return

    # reset timers and stuff
    def soft_reset(self):
        print("soft reset")

        # set disabled to quit all states and restart
        self.status = Mode.disabled
        self.BLUE.off()
        self.RED.off()
        self.GREEN.off()
        return

    # spawn a cloned process
    def hard_reset(self):
        print("hard reset")
        # import os
        # os.fork()
        # if (os.getpid() != 0):
        #     import sys
        #     sys.exit(0)
        return
