#Pi in the Sky
import time

import Adafruit_LSM303
import Adafruit_GPIO.SPI as SPI

lsm303 = Adafruit_LSM303.LSM303()
accelInitialized = None
accelInitCount = 0
accelInitSum = 0
accelConst = 0

while True:
    #getting accelerometer data
    accel, mag = lsm303.read()
    accel_x, accel_y, accel_z = accel

    #calibrating to earth's gravity
    if not accelInitialized:
        print("Calibrating...")
        accel_x, accel_y, accel_z = accel
        accelInitCount += 1
        accelInitSum += accel_z
        if accelInitCount == 50:
            accelInitialized = True
            accelConst = 9.81/(accelInitSum/50)
        
    #normal function
    else:
        accel_x = round((accel_x*accelConst),3)
        accel_y = round((accel_y*accelConst),3)
        accel_z = round((accel_z*accelConst),3)

        print(accel_z)
        time.sleep(0.1)
