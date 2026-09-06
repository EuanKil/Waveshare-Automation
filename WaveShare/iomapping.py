'''
    Pico I/O mapping as a Programmable Logic controller
    This file provides the digital input and output mapping to be used with the
    Raspberry Pico/Raspberry Pico W/Raspberry Pico 2/Raspberry Pico 2 W
    
    I/O mapping file as per the diagram Pico-OpenPLC-A4-Pinout.pdf
'''
import board
import digitalio

# ----- define the inputs and outputs
# INPUT I/O
IX0 = digitalio.DigitalInOut(board.GP6)
IX1 = digitalio.DigitalInOut(board.GP7)
IX2 = digitalio.DigitalInOut(board.GP8)
IX3 = digitalio.DigitalInOut(board.GP9)
IX4 = digitalio.DigitalInOut(board.GP10)
IX5 = digitalio.DigitalInOut(board.GP11)
IX6 = digitalio.DigitalInOut(board.GP12)
IX7 = digitalio.DigitalInOut(board.GP13)

IX0.direction = digitalio.Direction.INPUT
IX0.pull = digitalio.Pull.DOWN
IX1.direction = digitalio.Direction.INPUT
IX1.pull = digitalio.Pull.DOWN
IX2.direction = digitalio.Direction.INPUT
IX2.pull = digitalio.Pull.DOWN
IX3.direction = digitalio.Direction.INPUT
IX3.pull = digitalio.Pull.DOWN
IX4.direction = digitalio.Direction.INPUT
IX4.pull = digitalio.Pull.DOWN
IX5.direction = digitalio.Direction.INPUT
IX5.pull = digitalio.Pull.DOWN
IX6.direction = digitalio.Direction.INPUT
IX6.pull = digitalio.Pull.DOWN
IX7.direction = digitalio.Direction.INPUT
IX7.pull = digitalio.Pull.DOWN

# OUTPUT I/O
QX0 = digitalio.DigitalInOut(board.GP14)
QX1 = digitalio.DigitalInOut(board.GP15)
QX2 = digitalio.DigitalInOut(board.GP16)
QX3 = digitalio.DigitalInOut(board.GP17)
QX4 = digitalio.DigitalInOut(board.GP18)
QX5 = digitalio.DigitalInOut(board.GP19)
QX6 = digitalio.DigitalInOut(board.GP20)
QX7 = digitalio.DigitalInOut(board.GP21)

QX0.direction = digitalio.Direction.OUTPUT
QX1.direction = digitalio.Direction.OUTPUT
QX2.direction = digitalio.Direction.OUTPUT
QX3.direction = digitalio.Direction.OUTPUT
QX4.direction = digitalio.Direction.OUTPUT
QX5.direction = digitalio.Direction.OUTPUT
QX6.direction = digitalio.Direction.OUTPUT
QX7.direction = digitalio.Direction.OUTPUT
