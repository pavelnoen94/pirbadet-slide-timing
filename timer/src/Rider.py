import time

class Rider:
    time = int("inf")

    def start_time(self):
        self.time = time.time()

    def get_time(self):
        return time.time() - self.time

    def get_speed(self, distance):
        return distance/self.get_time()
