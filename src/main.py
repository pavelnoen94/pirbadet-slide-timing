#!/usr/bin/env python3
from Slide import Slide

def main():
    # TODO: start web server
    white_slide = Slide("hvit_sklie.ini")
    white_slide.start()

if __name__ == "__main__":
    main()
