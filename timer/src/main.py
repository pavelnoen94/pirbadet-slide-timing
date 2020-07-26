#!/usr/bin/env python3
import Slide, threading, signal, multiprocessing

terminator = multiprocessing.Event()


def main():

    # load configurations
    configurations = ["white_slide.ini"]
    threads = []
    # load all slides in threads and start
    for configuration in configurations:
        threads.append(threading.Thread(target=Slide.Slide, args=[configuration, terminator]))

    for thread in threads:
        thread.start()

    signal.signal(signal.SIGTERM, terminator_handler)
    signal.signal(signal.SIGINT, terminator_handler)

    if thread.is_alive():
        thread.join()

    return

def terminator_handler(arg1, arg2):
    terminator.set()

if __name__ == "__main__":
    main()
