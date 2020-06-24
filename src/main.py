#!/usr/bin/env python3
import Slide, threading, flask, json


def main():

    # load configurations
    configurations = ["white_slide.ini", "purple_slide.ini"]

    # set up web server and threds for slides
    api = flask.Flask(__name__)
    threads = []

    # load all slides in threads and start
    for configuration in configurations:
        threads.append(threading.Thread(target=Slide.Slide, args=[api, configuration]))

    for thread in threads:
        thread.start()

    # start the web server
    api.run(host="0.0.0.0")

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
