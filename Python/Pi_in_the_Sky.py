#Pi in the Sky
import time

import Adafruit_LSM303
import Adafruit_GPIO.SPI as SPI

import RPi.GPIO as GPIO

#pins for power and indicator LEDs
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

#accelerometer setup and variables
lsm303 = Adafruit_LSM303.LSM303()
state = 0
accelInitCount = 0
accelInitSum = 0
accelConst = 0

#gravity
G = 9.81

#variables for riemann sum calculation
rSumCount = 1
rSumData = []
rSumInit = 0
rSumEnd = 0
rSumCountdown = 0

#turns on the power LED to show that the program is running
GPIO.output(17, GPIO.HIGH)

running = True
while running:
    #getting accelerometer data
    accel, mag = lsm303.read()
    accel_x, accel_y, accel_z = accel

    #calibrating to earth's gravity
    if state == 0:
        accel_x, accel_y, accel_z = accel
        #gets the total acceleration magnitude
        accel_tot = ((accel_x**2)+(accel_y**2)+(accel_z**2))**(1/2)

        #counts up until 50 data points are collected for calibration
        accelInitCount += 1
        accelInitSum += accel_tot
        if accelInitCount == 50:
            #moves on to waiting for a throw
            state = 1
            #sets calibration constant
            accelConst = G/(accelInitSum/50)
            #blinks the power LED to show that its ready to be thrown
            GPIO.output(17, GPIO.LOW)
            time.sleep(1)
            GPIO.output(17, GPIO.HIGH)
        #these delays are required to prevent double readings
        time.sleep(0.02)
        
    #waiting for large enough acceleration to trigger data collection
    if state == 1:
        #gets calibrated acceleration magnitude
        accel_x = round((accel_x*accelConst),3)
        accel_y = round((accel_y*accelConst),3)
        accel_z = round((accel_z*accelConst),3)
        accel_tot = ((accel_x**2)+(accel_y**2)+(accel_z**2))**(1/2)
        accel_tot -= G

        #triggers next stage if it accelerates enough, as happens when thrown
        if accel_tot > 2:
            #changes state, records initial time for riemann sum
            state = 2
            rSumInit = time.time()
            rSumData.append(accel_tot)
            continue
    
    #gathering data
    if state == 2:
        #gets calibrated acceleration magnitude
        accel_x = round((accel_x*accelConst),3)
        accel_y = round((accel_y*accelConst),3)
        accel_z = round((accel_z*accelConst),3)
        accel_tot = ((accel_x**2)+(accel_y**2)+(accel_z**2))**(1/2)
        accel_tot -= G

        #continues to gather data until the acceleration drops too low
        if accel_tot > 1.5:
            rSumData.append(accel_tot)
            rSumCount += 1
            time.sleep(0.02)
            
        else:
            #performs trapezoidal riemann sum with the data gathered
            rSumEnd = time.time()
            rSumTime = (rSumEnd - rSumInit)/rSumCount
            rSumVel = (sum(rSumData)-(rSumData[0]/2)-(rSumData[len(rSumData)-1]/2))*rSumTime

            #turns off power LED, waits for the calculated time, then turns on indicator LED
            GPIO.output(17, GPIO.LOW)
            time.sleep(rSumVel/G)
            GPIO.output(24, GPIO.HIGH)

            #gives 2 seconds for the indicator, then ends the program
            time.sleep(2)
            GPIO.output(24, GPIO.LOW)
            running = False
