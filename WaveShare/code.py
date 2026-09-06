#import iomapping as IO # use this for the raspberry pico devices
#import iomapping_ws as IO # use this for the waveshare based board
from waveshare import PLC
#from raspberry import PLC  # use this for the Raspberyr Pico devices
import time
import asyncio
import simpleio


"""
   Comment out the two IO lines below if you use the iomapping/iomapping_ws versions of the library
   The iomapping/iomapping_ws libraries do now uses objects and only initialise the pins.
   The waveshare/raspberry libraries use objects and include additional functionality
   use the following two lines if you import the waveshare.py or raspberry.py
"""


IO = PLC()
IO.init_all()
IO.setServo()
IO.SERVO.angle = 0
print("Hello world")
COUNT = 0
IO.RGB_LED.fill((12,0,80)) #GRB

def mapto(v,x,y,a,b):
    #V: input value x y input range a,b: output range
    return (v-x) / (y-x) * (b-a) + a
    #plpot the voltage of the pot
    if RUNNING and (count % 30 ==0):
        v = (IO.IOW.value * 3.3) /65536
        #map to voltage 0-3-3v to temp 80-180deg
        t = mapto(v,0.0,3.3,80,180)
        a = mapto(t,80,180,0,180)
        IO.SERVO.angle = int(a)
        print(f"temp={t:0.2f}")

while True:
    
    START_BUTTON = IO.IX0.value 
    STOP_BUTTON = IO.IX1.value
    E_STOP = IO.IX5.value
    
    COUNT += 1
    # toggle a relay or output
    # start button
    if not IO.IX0.value and (COUNT % 30 == 0):
        IO.QX0.value = not IO.QX0.value
        IO.QX1.value = not IO.QX0.value
        IO.RGB_LED.fill((20,0,0)) # GRB
        # update waveshare.py to support the buzzer
        # .tone(port,frequency,length,duration)
        simpleio.tone(IO.BUZZER,262,0.25)
    # stop button
    if not IO.IX1.value and (COUNT % 30 == 0):
        IO.QX0.value = not IO.QX0.value
        IO.QX1.value = not IO.QX0.value
        IO.RGB_LED.fill((120,0,0)) #GRB
        simpleio.tone(IO.BUZZER,330,0.25)
    
    if not IO.IX2.value and (COUNT % 30 == 0):
        IO.QX0.value = not IO.QX0.value
        IO.QX1.value = not IO.QX0.value
        IO.RGB_LED.fill((120,0,0)) #GRB
        simpleio.tone(IO.BUZZER,330,0.25)
        
    if not IO.IX3.value and (COUNT % 30 == 0):
        IO.QX0.value = not IO.QX0.value
        IO.QX1.value = not IO.QX0.value
        IO.RGB_LED.fill((120,0,0)) #GRB
        simpleio.tone(IO.BUZZER,330,0.25)
    
    if not IO.IX4.value and (COUNT % 30 == 0):
        IO.QX0.value = not IO.QX0.value
        IO.QX1.value = not IO.QX0.value
        IO.RGB_LED.fill((120,0,0)) #GRB
        simpleio.tone(IO.BUZZER,330,0.25)


    # e-stop button
    if not IO.IX1.value:
        IO.RGB_LED.fill((0,250,0)) # GRB
        simpleio.tone(IO.BUZZER,500,0.25)
    IO.LED.value = not IO.LED.value # no LED on the waveshare board - uses RGB    
    time.sleep(0.010)
    IO.RGB_LED.show()
