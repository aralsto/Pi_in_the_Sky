#Pi in the Sky
import time

import Adafruit_LSM303
import Adafruit_GPIO.SPI as SPI

lsm303 = Adafruit_LSM303.LSM303()
state = 0
accelInitCount = 0
accelInitSum = 0
accelConst = 0

G = 9.81

while True:
    #getting accelerometer data
    accel, mag = lsm303.read()
    accel_x, accel_y, accel_z = accel

    #calibrating to earth's gravity
    if state == 0:
        print("Calibrating...")
        accel_x, accel_y, accel_z = accel
        accelInitCount += 1
        accelInitSum += accel_z
        if accelInitCount == 50:
            state = 1
            accelConst = G/(accelInitSum/50)
        
    #waiting for acceleration
    if state == 1:
        accel_x = round((accel_x*accelConst),3)
        accel_y = round((accel_y*accelConst),3)
        accel_z = round((accel_z*accelConst),3)
        accel_tot = ((accel_x**2)+(accel_y**2)+(accel_z**2))**(1/2)
        
        if accel_tot > 9.9:
            rSumStart = time.time()
            state = 2
    
    #calculating Riemann sum
    if state == 2:
        accel_x = round((accel_x*accelConst),3)
        accel_y = round((accel_y*accelConst),3)
        accel_z = round((accel_z*accelConst),3)
        accel_tot = ((accel_x**2)+(accel_y**2)+(accel_z**2))**(1/2)
        if accel_z > 10:
            rSumCount += 1
            rSum += accel_tot
        else:
            
