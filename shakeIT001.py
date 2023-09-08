import RPi.GPIO as GPIO
import time
import datetime

import sys
import os
import sqlite3

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)


def mainLoop():
    GPIO.output(21, GPIO.HIGH)
    print("21 HIGH Start")

    GPIO.output(20, GPIO.HIGH)
    print("20 HIGH Start")

    REST=10
    WAIT=1.5
    GPIO.output(21, GPIO.HIGH)
    GPIO.output(20, GPIO.HIGH)
            
    while True:    
            GPIO.output(21, GPIO.HIGH)
            GPIO.output(20, GPIO.LOW)
            print("21 HIGH 20 LOW")
            time.sleep(WAIT)

            GPIO.output(21, GPIO.HIGH)
            GPIO.output(20, GPIO.HIGH)
            print("21 HIGH 20 HIGH")
            time.sleep(REST)

            GPIO.output(21, GPIO.LOW)
            GPIO.output(20, GPIO.HIGH)
            print("21 LOW 20 HIGH")
            time.sleep(WAIT)
            
            GPIO.output(21, GPIO.HIGH)
            GPIO.output(20, GPIO.HIGH)
            print("21 HIGH 20 HIGH")
            time.sleep(REST)

def main():
  
    GPIO.setwarnings(False)

    try:
        mainLoop()

    
    except KeyboardInterrupt:
        
        GPIO.output(21, GPIO.HIGH)
        GPIO.output(20, GPIO.HIGH)
        print(" Quit")
        GPIO.cleanup()
            
    
if __name__ == '__main__':
    main()
    