import gpiozero, time, Rider, highscores
from enum import Enum
from Rider import Rider

class Mode(Enum):
    disabled = 1
    idle = 2
    running = 3


class Slide:
    # TODO: put inside a configuration file
    _MIN_TIME = 10 
    _MAX_TIME = 40

    # Outputs
    OUTPUT_GREEN_LED = gpiozero.LED(13)             # Green trffic light
    OUTPUT_RED_LED = gpiozero.LED(19)               # Red traffic light
    OUTPUT_BLUE_LED = gpiozero.LED(26)              # Someone is riding right now (for debugging)

    # Inputs
    INPUT_SENSOR_TOP = gpiozero.Button(24, pull_up=False)
    INPUT_SENSOR_BOTTOM = gpiozero.Button(16, pull_up=False)
    INPUT_RESET_HARD = gpiozero.Button(20, pull_up=False)          # clears current run and starts over again
    INPUT_RESET_SOFT = gpiozero.Button(21, pull_up=False)          # terminate the application and restart it
    INPUT_SWITCH_ENABLED = gpiozero.Button(6, pull_up=None, active_state=True)

    _rider = Rider()
    _status = Mode


    def load_configuration(self, configuration):
        # TODO: load configuration from file
        pass

        return


    def __init__(self, configuration=None):
        # enable reset button
        self.INPUT_RESET_SOFT.when_pressed = self.soft_reset
        self.INPUT_RESET_HARD.when_pressed = self.hard_reset
        self.INPUT_SWITCH_ENABLED.when_released = self.disabled

        # TODO: signal interupt handler
        # TODO: load highscores

        self.load_configuration(configuration)
        return

    def mode_selector(self):
        if(not self.INPUT_SWITCH_ENABLED.is_pressed):
            self.disabled()
            return
        self._status = Mode.idle

    def start(self):
        self.mode_picker()


    def mode_picker(self):
        print("mode picker")
        while (True):
            self.mode_selector()
            if(self._status == Mode.idle):
                self.idle()
            if(self._status == Mode.running):
                self.running()

        return


    def disabled(self):
        print("disabled")

        # turn off lights
        self.OUTPUT_GREEN_LED.off()
        self.OUTPUT_RED_LED.off()
        self.OUTPUT_BLUE_LED.off()
        # wait for enable switch
        while (not self.INPUT_SWITCH_ENABLED.is_pressed):
            pass

        print("enabled")
        self._status = Mode.idle
        return


    def idle(self):
        print("idle")

        # Green light!
        self.OUTPUT_RED_LED.off()
        self.OUTPUT_GREEN_LED.on()

        # wait for a rider
        while (not self.INPUT_SENSOR_TOP.is_pressed):
            # return if interupted by reset or disable
            if (self._status != Mode.idle):
                return

        # Red light! Start timer
        self._rider.start_time()
        self.OUTPUT_RED_LED.on()
        self.OUTPUT_GREEN_LED.off()

        self._status = Mode.running
        return


    def running(self):
        print("running")

        # indicate that someone is riding
        self.OUTPUT_BLUE_LED.on()

        # wait for a user to exit the track.
        while (not self.INPUT_SENSOR_BOTTOM.is_pressed):
            if (self._status != Mode.running):
                return

        # print time and speed
        currentTime = self._rider.get_time()
        print("time: " + str(round(currentTime,2)) + "s")
        currentSpeed = self._rider.get_speed(100) # assuming the slide is 100m long
        print("speed: " + str(round(currentSpeed,2)) + "m/s")


        self.OUTPUT_BLUE_LED.off()
        self._status = Mode.idle

        return

    # reset timers and stuff
    def soft_reset(self):
        print("soft reset")

        # set disabled to quit all states and restart
        self._status = Mode.disabled
        self.OUTPUT_BLUE_LED.off()
        self.OUTPUT_RED_LED.off()
        self.OUTPUT_GREEN_LED.off()
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
