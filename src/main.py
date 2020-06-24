#!/usr/bin/env python3
from Slide import Slide
import threading

def main():
    # TODO: start web server
    
    configurations = ["white_slide.ini", "purple_slide.ini"]
    threads = []

    for configuration in configurations:
        threads.append(threading.Thread(target=Slide, args=[configuration]))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
