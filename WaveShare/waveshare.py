"""
    I/O mapping as a Programmable Logic controller
    This  file provides the digital input and output mapping to be used with
    the Waveshare relay board.
    
    version 1.2

"""

import os
import sys
import time

# Make sure a pico is attached before trying to use the library
import analogio
import board
import busio
import digitalio
import pwmio
import neopixel
import pwmio
from adafruit_motor import servo

# import adafruit_ssd1306

# uart = usb_cdc.console
# UART = usb_cdc.data
class PLC:
    # ---- picoPLC addtional I/O MAPPING
    # one wire support for Dallas devices, DHT, etc.
    ONEWIRE = board.GP47

    # group the inputs and outputs into lists for easy access
    GPIN: list = [digitalio.DigitalInOut] * 8
    GPOUT: list = [digitalio.DigitalInOut] * 8

    # I2C,SPI & UART
    # - I2C
    SDA = board.GP6  # data out
    SCL = board.GP7  # data in
    RTC_SDA = SDA
    RTC_SCL = SCL
    RTC_INT = board.GP8

    BUZZER = board.GP3
   
    
    # - SPI
    SPI_RX = board.GP28
    SPI_CS = board.GP31
    SPI_SCK = board.GP26
    SPI_TX = board.GP27

    # - UART
    RS485_TX = board.GP4
    RS485_RX = board.GP5
    UART_TX = board.GP0
    UART_RX = board.GP1

    OLEDw = 128
    OLEDh = 64
    OLEDlines = 6  # lines of text on the OLED
    OLEDdata = [""] * OLEDlines

    def __init__(self):
        self.LED: digitalio.DigitalInOut = digitalio.DigitalInOut(board.LED)
        self.LED.direction = digitalio.Direction.OUTPUT
        #self.BUZZER = digitalio.DigitalInOut(board.GP3)
        #self.BUZZER.direction = digitalio.Direction.OUTPUT
        self.IW0 = self.ADC0 = analogio.AnalogIn(board.GP40)
        self.IW1 = self.ADC1 = analogio.AnalogIn(board.GP41)
        self.IW2 = self.ADC2 = analogio.AnalogIn(board.GP42)

        self.AOUT0 = self.PWM0 = self.QW0 = None
        self.AOUT1 = self.PWM1 = self.QW1 = None
        self.SERVO = None
        self._servo = None

        # 1 pixel RGB led
        self.RGB_LED = neopixel.NeoPixel(board.GP2, 1, brightness=0.1)
        self.RGB_LED.fill((0, 0, 0))
        self.RGB_LED.show()

        # assume no peripherals are set or attached
        self.UART = self.I2C = self.OLED = self.SPI = None
        self.setGPIO()

    def init_all(self):
        """Initialiase the peripheral interfaces as a group

        I2C, SPI, UART, OLED
        """
        self.setI2C()
        self.setSPI()
        self.setUART()
        self.setPWM()  # default to 1KHz

        try:
            self.setOLED(self.OLEDw, self.OLEDh)
        except:
            print("No OLED")
 
    def setServo(self):
        if not self._servo is None:
            self._servo.deinit() 
        
        try:
            self._servo = pwmio.PWMOut(
                board.GP39, duty_cycle=2 ** 15, frequency=50, variable_frequency=True
            )
            self.SERVO = servo.Servo(self._servo)
            print(f"Initialising servo PWM to 50Hz on board.GP39")
            print("- this overrides the freq. of QW0 and QW1")

        except:
            print(
                "Error setting the servo PWM to 50Hz on board.GP39"
            )
            self.SERVO = None

            return
        
    def setPWM(self, freq=1000):
        """Initialise the PWM frequency and IO pins

        Both channels are set at the same time as they share the same PWM slice.
        """
        if not self.QW0 is None:
            self.QW0.deinit()
        if not self.QW1 is None:
            self.QW1.deinit()
 
        try:
            self.QW0 = pwmio.PWMOut(
                board.GP43, duty_cycle=0, frequency=freq, variable_frequency=True
            )
            self.QW1 = pwmio.PWMOut(
                board.GP44, duty_cycle=0, frequency=freq, variable_frequency=True
            )
            print(
                f"Initialising PWM to {freq}Hz on board.GP43 & board.GP44"
            )

        except:
            print(
                "Error setting the PWM to {freq}Hz on board.GP37 & board.GP38"
            )
            self.AOUT0 = self.PWM0 = self.QW0 = None
            self.AOUT1 = self.PWM1 = self.QW1 = None
            return
        self.AOUT0 = self.PWM0 = self.QW0
        self.AOUT1 = self.PWM1 = self.QW1

    def setSPI(self):
        """Initialiase the SPI on GP2,GP3,GP4,GP5"""
        pass

    def setI2C(self):
        """Initialise the I2C on GP0,GP1 @ 400KHz"""
        print(f"Initialising the I2C on {self.SCL},{self.SDA} @ 400KHz")
        try:
            self.I2C = busio.I2C(self.SCL, self.SDA, frequency=400_000)
            poll = 0
            while not self.I2C.try_lock() and poll < 10:
                poll += 1
            print(
                "I2C addresses found:",
                [hex(device_address) for device_address in self.I2C.scan()],
            )
            self.I2C.unlock()

        except:
            self.I2C = None
            print("No I2C device attached")

    def setUART(self, baud=115200):
        """Initialiase the UART on GP4,GP5 @ 115200 baud"""
        print(
            f"Initialising UART to {baud} baud on {self.UART_TX} & {self.UART_RX}"
        )
        try:
            self.UART = busio.UART(
                self.UART_TX, self.UART_RX, baudrate=115200, timeout=1
            )
        except:
            print("No UART capability found")
            self.UART = None

    def setGPIO(self):
        """Initialiase the I/O on GP6-GP13 for input and GP14-GP21 for output

        IX0-IX7 for inputs

        QX0-QX7 for outputs
        """

        # ----- define the inputs and outputs
        ipins = [
            board.GP9,
            board.GP10,
            board.GP11,
            board.GP12,
            board.GP13,
            board.GP14,
            board.GP15,
            board.GP16,
        ]

        opins = [
            board.GP17,
            board.GP18,
            board.GP19,
            board.GP20,
            board.GP21,
            board.GP22,
            board.GP23,
            board.GP24,
        ]

        print(f"Initialising the GPIO on GP6-GP13 for input and GP14-GP21 for output")
        for v in range(8):
            # create output pins
            self.GPOUT[v] = digitalio.DigitalInOut(opins[v])
            self.GPOUT[v].direction = digitalio.Direction.OUTPUT
            self.GPOUT[v].value = False
            self.QX0: digitalio.DigitalInOut = self.GPOUT[0]
            self.QX1: digitalio.DigitalInOut = self.GPOUT[1]
            self.QX2: digitalio.DigitalInOut = self.GPOUT[2]
            self.QX3: digitalio.DigitalInOut = self.GPOUT[3]
            self.QX4: digitalio.DigitalInOut = self.GPOUT[4]
            self.QX5: digitalio.DigitalInOut = self.GPOUT[5]
            self.QX6: digitalio.DigitalInOut = self.GPOUT[6]
            self.QX7: digitalio.DigitalInOut = self.GPOUT[7]

            # create input pins
            self.GPIN[v] = digitalio.DigitalInOut(ipins[v])
            self.GPIN[v].direction = digitalio.Direction.INPUT
            self.GPIN[v].pull = digitalio.Pull.DOWN
            self.IX0: digitalio.DigitalInOut = self.GPIN[0]
            self.IX1: digitalio.DigitalInOut = self.GPIN[1]
            self.IX2: digitalio.DigitalInOut = self.GPIN[2]
            self.IX3: digitalio.DigitalInOut = self.GPIN[3]
            self.IX4: digitalio.DigitalInOut = self.GPIN[4]
            self.IX5: digitalio.DigitalInOut = self.GPIN[5]
            self.IX6: digitalio.DigitalInOut = self.GPIN[6]
            self.IX7: digitalio.DigitalInOut = self.GPIN[7]

    def setOLED(self, W: int = 128, H: int = 64):
        import sh1106  # works for the ssd1306 driver chips too

        """Initialiase the OLED on the I2C
            SH1106 OLED with 128x64 resolution
        Args:
            W (int): OLED width in pixels. default 128
            H (int): OLED height in pixels. default 64
        """

        if not self.I2C:
            return
        if not self.OLED is None:
            del self.OLED
        print(f"Initialising the {W}xGP{H} OLED on I2C0")
        try:
            self.OLED = sh1106.SH1106_I2C(W, H, self.I2C, addr=0x3C)
        except:
            self.OLED = None
            print("No OLED attached")

    """
    def OLEDtext(self,line:int,strs:list):
        if not self.OLED: return 
        if not isinstance(strs,list): return        
        if line in (0,1,2,3,4,5):
            self.OLED.fill(False)
            for i in range(5):
                #try:
                 if len(strs[i]) > 0:
                    self.OLEDdata[i] = strs[i]
                    self.OLED.text(strs[i],0,line * 10,1)
                #except: 
                #    return
            self.OLED.show()        
    """

    # display 1 or more lines of text from a list onto the OLED
    def display(self, strs: list):
        """Send 1-6 strings to the OLED display assuming the 128x64 device

        Args:
            strs (list): List of 1-6 strings
        """
        if not self.OLED:
            return
        if not isinstance(strs, list):
            return
        if len(strs) > self.OLEDlines:
            strs = strs[: self.OLEDlines]
        self.OLED.fill(False)
        for k, v in enumerate(strs):
            try:
                # save updated line
                if len(v) > 0:
                    self.OLEDdata[k] = v
                self.OLED.text(self.OLEDdata[k], 0, k * 10, 1)
            except:
                return
        self.OLED.show()

    def testOLED(self):
        """Print a test message on the OLED"""

        if not self.I2C:
            self.setOLED(128, 64)
            # self.OLED = adafruit_ssd1306.SSD1306_I2C(128, 64, self.I2C) # 0.96" OLED
        if not self.OLED:
            return

        self.OLED.fill(False)
        self.OLED.text("Hello world!", 0, 0, 1)
        self.OLED.text("picoXpander", 0, 10, 1)
        self.OLED.text("Version 1.0", 0, 20, 1)
        self.OLED.show()

    def map_range(
        self, value: int, in_min: int, in_max: int, out_min: int, out_max: int
    ) -> int:
        """Map a value from one range to another

        Args:
            value (int): value to map
            in_min (int): low end of from range
            in_max (int): upper end of from range
            out_min (int): low end of to range
            out_max (int): upper end of to range

        Returns:
            int: mapped integer
        """
        return (value - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

    def map_range_zero(self, value: int, in_max: int, out_max: int) -> int:
        """Map a value from one range to another assuming the ranges start at 0

        Args:
            value (int): value to map
            in_max (int): upper end of from range
            out_max (int): upper end of to range

        Returns:
            int: mapped integer
        """
        return value * out_max // in_max


def pollOut(plc: PLC, delay: float):
    """Test the Outputs"""
    for i in range(8):
        plc.GPOUT[i].value = True
        time.sleep(delay)
        plc.GPOUT[i].value = False


def pollIn(plc: PLC, delay: float):
    """Test the inputs"""

    toggle = False
    # scan through the inputs
    for i in range(8):
        # if the input is high toggle the out twice
        if plc.GPIN[i].value:
            plc.GPOUT[i].value = True
            time.sleep(delay)
            plc.GPOUT[i].value = False
            time.sleep(delay)
            plc.GPOUT[i].value = True
            time.sleep(delay)
            plc.GPOUT[i].value = False
            toggle = True
            time.sleep(delay)

    return toggle


# diagnostics test code
if __name__ == "__main__":
    import random

    plc = PLC()
    plc.init_all()
    plc.testOLED()
    time.sleep(1)
    flag = True
    while True:
        GRB = (random.randint(0, 254), random.randint(0, 254), random.randint(0, 254))
        plc.RGB_LED[0] = GRB  # 1 pixel
        plc.RGB_LED.show()
        # keep scanning whilst there is an input
        flag = pollIn(plc, 0.1)

        if not flag:
            # pollOut(0.2)
            pollOut(plc, 0.05)

        # these lines used to confirm code is running in the loop
        plc.LED.value = not plc.LED.value
        time.sleep(1.0)
