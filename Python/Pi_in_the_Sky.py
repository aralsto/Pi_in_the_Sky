#Pi in the Sky
import time

import Adafruit_LSM303
import Adafruit_GPIO.SPI as SPI

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

lsm303 = Adafruit_LSM303.LSM303()
state = 0
accelInitCount = 0
accelInitSum = 0
accelConst = 0

G = 9.81

#sumsusmusmusm = 0
#file = open("/home/pi/Documents/Pi_in_the_Sky/data.txt","w")
#file.write("whyisitweird \n")

rSumCount = 1
rSumData = []
rSumInit = 0
rSumEnd = 0
rSumCountdown = 0
GPIO.output(17, GPIO.HIGH)

running = True
while running:
    #getting accelerometer data
    accel, mag = lsm303.read()
    accel_x, accel_y, accel_z = accel

    #calibrating to earth's gravity
    if state == 0:
        #print("Calibrating...")
        #file.write("Calibrating... \n")
        accel_x, accel_y, accel_z = accel
        accel_tot = ((accel_x**2)+(accel_y**2)+(accel_z**2))**(1/2)
        accelInitCount += 1
        accelInitSum += accel_tot
        if accelInitCount == 50:
            state = 1
            #print("done")
            accelConst = G/(accelInitSum/50)
            GPIO.output(17, GPIO.LOW)
            time.sleep(1)
            GPIO.output(17, GPIO.HIGH)
        time.sleep(0.02)
        
    #waiting for trigger
    if state == 1:
        accel_x = round((accel_x*accelConst),3)
        accel_y = round((accel_y*accelConst),3)
        accel_z = round((accel_z*accelConst),3)
        accel_tot = ((accel_x**2)+(accel_y**2)+(accel_z**2))**(1/2)
        accel_tot -= G
        #file.write(str(accel_tot)+"\n")
        #sumsusmusmusm += 1
        #if sumsusmusmusm > 100:
            #running = False
            #GPIO.output(17, GPIO.LOW)
            #file.close()
        #print(accel_tot)
        if accel_tot > 2:
            state = 2
            rSumInit = time.time()
            rSumData.append(accel_tot)
            #print("changed")
            #file.write("changed \n")
            continue
    
    #gathering data
    if state == 2:
        #GPIO.output(17, GPIO.HIGH)
        accel_x = round((accel_x*accelConst),3)
        accel_y = round((accel_y*accelConst),3)
        accel_z = round((accel_z*accelConst),3)
        accel_tot = ((accel_x**2)+(accel_y**2)+(accel_z**2))**(1/2)
        accel_tot -= G
        #file.write(str(accel_tot)+"\n")
        #print(accel_tot)
        if accel_tot > 1.5:
            rSumData.append(accel_tot)
            rSumCount += 1
            time.sleep(0.02)
            
        else:
            rSumEnd = time.time()
            #file.write("CHANGED AGAIN")
            #print("CHANGED AGAIN")
            rSumTime = (rSumEnd - rSumInit)/rSumCount
            rSumVel = (sum(rSumData)-(rSumData[0]/2)-(rSumData[len(rSumData)-1]/2))*rSumTime
            #file.write(str(rSumVel/G))
            #print(rSumVel/G)
            #file.close()
            GPIO.output(17, GPIO.LOW)
            time.sleep(rSumVel/G)
            GPIO.output(24, GPIO.HIGH)
            time.sleep(2)
            GPIO.output(24, GPIO.LOW)
            running = False
