"""
I/O mapping as a Programmable Logic controller
This file provides the digital input and output mapping for the Waveshare relay board

I/O mapping file as per the RP2350B_Relay_board_GPIO.xlsx spreadsheet
"""

import analogio
import board
import busio
import digitalio
import pwmio
import usb_cdc

# uart = usb_cdc.console
UART = usb_cdc.data

# ---- picoPLC addtional I/O MAPPING
ONEWIRE = board.GP47

# onboard led used for runtime activity
LED = digitalio.DigitalInOut(board.LED)
LED.direction = digitalio.Direction.OUTPUT

RGB_LED = digitalio.DigitalInOut(board.GP2)
RGB_LED.direction = digitalio.Direction.OUTPUT

BUZZER = board.GP3
# BUZZER = digitalio.DigitalInOut(board.GP3)
# BUZZER.direction = digitalio.Direction.OUTPUT

RS485_TX = board.GP4
RS485_RX = board.GP4
UART_TX = board.GP0
UART_RX = board.GP1

# analogue outputs & PWM - defaults to 1KHz
QW0 = pwmio.PWMOut(board.GP37, duty_cycle=2**15, frequency=1000)
QW1 = pwmio.PWMOut(board.GP38, duty_cycle=2**15, frequency=1000)
PWM1 = AOUT1 = QW0
PWM2 = AOUT2 = QW1

# analogue inputs
IW0 = analogio.AnalogIn(board.GP40)
IW1 = analogio.AnalogIn(board.GP41)
IW2 = analogio.AnalogIn(board.GP42)
ADC0 = IW0
ADC1 = IW1
ADC2 = IW2

# I2C & UART
SDA = TX = board.GP6  # data out
SCL = RX = board.GP7  # data in
RTC_SDA = SDA
RTC_SCL = SCL
RTC_INT = board.GP8

# SPI
SPI_RX = board.GP28
SPI_CS = board.GP31
SPI_SCK = board.GP26
SPI_TX = board.GP27

# setup the I2C interface - default 400KHz
try:
    I2C = busio.I2C(board.SCL_ALT, board.SDA_ALT, frequency=100000)
    while not I2C.try_lock():
        pass
    print(
        "I2C addresses found:", [hex(device_address) for device_address in I2C.scan()]
    )
    I2C.unlock()
except Exception as e:
    print(f"Error:{e}")

# ----- define the inputs and outputs
# INPUT I/O
IX0 = digitalio.DigitalInOut(board.GP9)
IX1 = digitalio.DigitalInOut(board.GP10)
IX2 = digitalio.DigitalInOut(board.GP11)
IX3 = digitalio.DigitalInOut(board.GP12)
IX4 = digitalio.DigitalInOut(board.GP13)
IX5 = digitalio.DigitalInOut(board.GP14)
IX6 = digitalio.DigitalInOut(board.GP15)
IX7 = digitalio.DigitalInOut(board.GP16)

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
QX0 = digitalio.DigitalInOut(board.GP17)
QX1 = digitalio.DigitalInOut(board.GP18)
QX2 = digitalio.DigitalInOut(board.GP19)
QX3 = digitalio.DigitalInOut(board.GP20)
QX4 = digitalio.DigitalInOut(board.GP21)
QX5 = digitalio.DigitalInOut(board.GP22)
QX6 = digitalio.DigitalInOut(board.GP23)
QX7 = digitalio.DigitalInOut(board.GP24)

QX0.direction = digitalio.Direction.OUTPUT
QX1.direction = digitalio.Direction.OUTPUT
QX2.direction = digitalio.Direction.OUTPUT
QX3.direction = digitalio.Direction.OUTPUT
QX4.direction = digitalio.Direction.OUTPUT
QX5.direction = digitalio.Direction.OUTPUT
QX6.direction = digitalio.Direction.OUTPUT
QX7.direction = digitalio.Direction.OUTPUT
