#!/usr/bin/env python3
from Slide import Slide
import threading

def main():
    # TODO: start web server
    white_slide = Slide("white_slide.ini")
    purple_slide = Slide("purple_slide.ini")
    
    thread1 = threading.Thread(target=white_slide.start)
    thread2 = threading.Thread(target=purple_slide.start)

    threads = []

    threads.append(thread1)
    threads.append(thread2)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
