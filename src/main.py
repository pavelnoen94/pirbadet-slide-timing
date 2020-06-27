#!/usr/bin/env python3
import Slide, threading


def main():

    # load configurations
    configurations = ["white_slide.ini"]
    threads = []

    # load all slides in threads and start
    for configuration in configurations:
        threads.append(threading.Thread(target=Slide.Slide, args=[configuration]))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    return


if __name__ == "__main__":
    main()
