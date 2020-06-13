import time

class Rider:
    start = None
    
    def start(self):
        self.start = time.time()

    def get_time(self):
        return time.time() - start
