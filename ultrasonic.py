#Libraries
import RPi.GPIO as GPIO
import time
import os
import random

trumps = ['1.wav', '3.wav', '3.wav', '4.wav']


#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_LED=23
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_LED, GPIO.OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    cnt =0
    try:
        while True:
            dist = distance()

            wav = random.choice(trumps)
            print ("Measured Distance = %.1f cm cnt=%d wav=%s" % (dist,cnt,wav))
            
            cmd = "aplay {0}".format(wav)
		 
            if (dist <= 64) :
                time.sleep(2)
                GPIO.output(GPIO_LED, GPIO.HIGH)          
                os.system(cmd)
                cnt+=1
                
            time.sleep(1)
            GPIO.output(GPIO_LED, GPIO.LOW)          
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()