import gpiozero, time, Rider, configparser, highscores, signal, mqtt
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

        self.mqtt = mqtt.message_sender(self.name, self.mqtt_server)

        self.highscore = highscores.high_scores(self.name, self.mqtt)
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

        self.mqtt_server = str(config["SERVER"]["mqtt"])
        self.name = config["DEFAULT"]["name"]
        self.rider = Rider()
        self.status = Mode

        print("[Info]: Loaded configuration: " + self.name)

        return


    def interupt_sensor_top(self):
        if(self.status != Mode.idle):
            return
        if(self.status == Mode.disabled):
            return

        self.rider.start_time()
        self.status = Mode.running

        self.mqtt.send("status","busy")

        self.GREEN_LED.off()
        self.RED_LED.on()

        return


    def interupt_sensor_bottom(self):
        if(self.status == Mode.idle):
            return
        if(self.rider.get_time() < self.MIN_TIME):
            return
        if(self.rider.get_time() > self.MAX_TIME):
            return

        time = round(self.rider.get_time(),2)
        speed = round(self.rider.get_speed(self.distance),2)

        if(self.status != Mode.disabled):
            self.mqtt.send("status", "empty")

        self.highscore.add_result(time, speed)
        self.mqtt.send_obj("high_score" ,self.highscore.highscores)

        if(self.status == Mode.disabled):
            return

        self.status = Mode.idle
        self.GREEN_LED.on()
        self.RED_LED.off()

        return


    def interupt_soft_reset(self):
        if(self.status == Mode.disabled):
            return
        self.mqtt.send("status", "reset")
        self.status = Mode.idle
        self.GREEN_LED.on()
        self.RED_LED.off()

        return

    def interupt_reset_highscores(self):
        self.mqtt.send("status", "reset high score")
        self.highscore.reset()
        self.mqtt.send_obj("high_score" ,self.highscore.highscores)
        return


    def mqtt_receiver(self, client, userdata, message):
        command = str(message.payload)[2:-1]

        if (command == "reset"):
            self.interupt_soft_reset()
            return

        if (command == "disable"):
            self.mqtt.send("status","disabled")
            self.disable_handler()
            return

        if (command == "enable"):
            self.mqtt.send("status","enabled")
            self.enable_handler()
            return
        if (command == "reset_high_score"):
            self.mqtt.send("status","reset highs core")
            self.highscore_reset_handler()
            return

        return


    def highscore_reset_handler(self):
        self.highscore.reset()


    def disable_handler(self):
        if(self.status == Mode.disabled):
            return

        # If the slide is busy: don't do anything
        if(self.status == Mode.running):
            self.status = Mode.disabled
            return

        # If the slide is free: set red light
        if(self.status == Mode.idle):
            self.GREEN_LED.off()
            self.RED_LED.on()
            self.status = Mode.disabled

        return


    def enable_handler(self):
        # if the slide isn't disabled, don't do anything.
        if(self.status != Mode.disabled):
            if (self.rider.get_time() < self.MAX_TIME and self.rider.get_time() > self.MIN_TIME):
                # Someone is inside the slide right now
                self.status = Mode.running
                return

            # Slide is empty. Go idle.
            self.status = Mode.idle
            self.GREEN_LED.on()
            self.RED_LED.off()

        return


    def start(self):
        self.mqtt.loop_start()
        self.mqtt.subscribe("action")
        self.mqtt.message_callback_add("action", self.mqtt_receiver)
        self.mqtt.send("status", "active")
        self.TOP.when_pressed = self.interupt_sensor_top
        self.BOTTOM.when_pressed = self.interupt_sensor_bottom

        self.status = Mode.idle
        self.GREEN_LED.on()

        # FIXME: this is ugly
        while not self.termination_signal.is_set():
            try:
                if (self.status == Mode.running) and (self.rider.get_time() > self.MAX_TIME):
                    self.interupt_soft_reset()
            except TypeError:
                pass
            time.sleep(1)

        self.quit()
        return


    def quit(self):
        self.highscore.save_highscores()
        self.mqtt.send("status", "shut down")
        self.mqtt.loop_stop()
        self.mode = Mode.quitting
