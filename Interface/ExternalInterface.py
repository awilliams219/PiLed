from Data.Colors import Colors


class ExternalInterface:
    LED = None

    def __init__(self, LED):
        self.LED = LED

    def setLED(self, LED):
        self.LED = LED

    def blink(self, interval, color1, color2):
        if self.LED is not None:
            self.LED.disableBlink()
            self.LED.enableBlink(interval, color1, color2)

    def off(self):
        if self.LED is not None:
            self.LED.disableBlink()
            self.LED.setColor(Colors.Black)

    def setColor(self, color):
        if self.LED is not None:
            self.LED.disableBlink()
            self.LED.setColor(color)

    def sequence(self, interval, colors):
        if self.LED is not None:
            self.LED.disableBlink()
            self.LED.sequence(interval, colors)

    def getColors(self):
            return Colors.NamedAll

    @staticmethod
    def terminate():
        exit(0)
