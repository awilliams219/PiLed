from Data.Colors import Colors
from Tools.Interval import Interval
from collections import deque


class StatusLED:

    Color = Colors.Off
    AltColor = Colors.Off
    Blinking = False
    BlinkInterval = 0
    GPIODriver = None
    Timer = None
    Lit = False

    def __init__(self, GPIODriver, Configuration):
        self.GPIODriver = GPIODriver
        self.LEDArray = list(Configuration.GPIO.Leds.values())
        self.Configuration = Configuration

    def setColor(self, newColor):
        self.Color = newColor
        self.__setPins(newColor)
        if newColor == Colors.Off:
            self.Lit = False
        else:
            self.Lit = True

    def enableBlink(self, interval=0.5, color1=Colors.Off, color2=Colors.Off):
        if not self.Blinking:
            self.Color = color1
            self.AltColor = color2
            self.Blinking = True
            self.BlinkInterval = interval
            self.Timer = Interval(self.BlinkInterval, self.__toggle, None)

    def disableBlink(self):
        if self.Blinking:
            self.Timer.cancel()
            self.Blinking = False

    def sequence(self, interval, colors):
        if type(colors) is not deque:
            if isinstance(colors, (list, tuple)):
                self.sequence(interval, deque(colors))
            else:
                print("Invalid Sequence Definition")

            return

        self.Blinking = True
        self.setColor(colors[0])
        colors.rotate(1)
        self.Timer = Interval(interval, self.sequence, interval, colors)

    def __toggle(self, params):
        self.Color, self.AltColor = self.AltColor, self.Color
        self.setColor(self.Color)
        self.Timer = Interval(self.BlinkInterval, self.__toggle, None)

    def __setPins(self, color):
        redPin = self.GPIODriver.HIGH if bool(Colors.Red & color) else self.GPIODriver.LOW
        greenPin = self.GPIODriver.HIGH if bool(Colors.Green & color) else self.GPIODriver.LOW
        bluePin = self.GPIODriver.HIGH if bool(Colors.Blue & color) else self.GPIODriver.LOW

        self.GPIODriver.output(self.Configuration.GPIO.Leds["Red"], redPin)
        self.GPIODriver.output(self.Configuration.GPIO.Leds["Green"], greenPin)
        self.GPIODriver.output(self.Configuration.GPIO.Leds["Blue"], bluePin)
