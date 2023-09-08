import RPi.GPIO as GPIO
import time
import datetime

import sys
import os
import sqlite3

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT) # Petierelementet
GPIO.setup(21, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)

#28-3c01d607311e

def read(ds18b20):
    try:
      location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
      tfile = open(location)
      text = tfile.read()
      tfile.close()
      secondline = text.split("\n")[1]
      temperaturedata = secondline.split(" ")[9]
      temperature = float(temperaturedata[2:])
      celsius = temperature / 1000
    #farenheit = (celsius * 1.8) + 32
    except IndexError:
    #  print("Läsningsfel")  
      celsius = 0
      
    return celsius



def readOutsideTemp():
    locationValue = "28-01192dfdfd7e"
    #locationValue = "28-3c01b556f4b5"

    originalTemp = read(locationValue)
    
    global tempA

    tempA = originalTemp 

    return tempA



def readInsideTemp():
    locationValue = "28-0120332d4057"
    #locationValue = "28-0120335e17d4"

    originalTemp = read(locationValue)

    global tempB

    tempB = originalTemp 

    return tempB
    
def readOmgivTemp():
    locationValue = "28-3c01d607311e"
    #locationValue = "28-0120335e17d4"

    originalTemp = read(locationValue)

    global tempC

    tempC = originalTemp 

    return tempC

def mainLoop():
    GPIO.output(16, GPIO.HIGH)
    GPIO.output(20, GPIO.HIGH)
    GPIO.output(21, GPIO.HIGH)


 # Opening a file
    print ("Oppna fil")
    global file1
    file1 = open('logpump1.txt', 'w')
    s = "Time;TempA;TempB\n"
 # Writing a string to file
    file1.write(s)

    varv = 0
    rtemp=0

    print("HIGH Start")

  
    while True:
  
      GPIO.output(16, GPIO.HIGH) # Inget pertier
      GPIO.output(20, GPIO.HIGH)

      GPIO.output(21, GPIO.LOW)  # Ingen tempoverf
      print("Ingen temp overf")
      time.sleep(2)
      GPIO.output(21, GPIO.HIGH)
 
 
      while True:
            readOutsideTemp()
            readInsideTemp()
            readOmgivTemp()         
            time.sleep(0.5)
            print("TTTRULtempA",tempA)
            print("TTTRULtempB",tempB)      
            print("TTTRULtempC",tempC) 

            print ("Varv",varv)
            varv = varv + 1 
            AA=str(round(tempA,2))
            BB=str(round(tempB,2))
            VV=str(varv)
            file1.write(VV+";"+AA+";"+BB+"\n")


    
            if(( tempA < (tempC + 5) and tempA  != 0) and rtemp == 0)  or (rtemp == 1 and tempB > 16.5 and tempB != 0) :
              if rtemp == 1 and tempB > 16.5 :
                  rtemp=0
              break
 
 
      print("ON")

        
      GPIO.output(20, GPIO.LOW)  # Tempoverf
      print("Temp overf")
      time.sleep(2)
      GPIO.output(20, GPIO.HIGH)
 
      GPIO.output(16, GPIO.LOW)     # Pertier aktiv
      GPIO.output(20, GPIO.HIGH)
 
      while True:
            readOutsideTemp()
            readInsideTemp()
            readOmgivTemp()  
            time.sleep(0.5)
            print("TRULtempA",tempA)
            print("TRULtempB",tempB)   
            print("TRULtempC",tempC) 

            print ("Varv",varv)
            varv = varv + 1  
            AA=str(round(tempA,2))
            BB=str(round(tempB,2))
            VV=str(varv)
            file1.write(VV+";"+AA+";"+BB+"\n")


       
            if (tempA > (tempC + 5) and (tempC  != 0))   or ((tempB < 16) and (tempB  != 0)) :
              if tempB<16:
                  rtemp=1
              else :
                   rtemp=0                 
              break
 

 
def main():
  
    GPIO.setwarnings(False)
 



    try:
        mainLoop()

        global file1
        file1.close()

    
    except KeyboardInterrupt:
        
        GPIO.output(16, GPIO.HIGH)
        GPIO.output(20, GPIO.HIGH)       
        GPIO.output(21, GPIO.HIGH)        
        
        print(" Quit")
        GPIO.cleanup()

        file1.close()           
    
if __name__ == '__main__':
    main()
    