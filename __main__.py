from Data.Colors import Colors
import RPi.GPIO as GPIODriver
from Driver.StatusLED import StatusLED
from time import sleep
from Interface.ExternalInterface import ExternalInterface
import socket
import errno
import signal
import zerorpc
import zc.lockfile

PORT = 4242
LOCKFILE = None

Leds = {
    "Red": 16,
    "Green": 20,
    "Blue": 21
}

class GPIO:
    Leds = Leds


class Configuration:
    GPIO = GPIO


def main(args=None):
    global LOCKFILE
    signal.signal(signal.SIGINT, destruct)

    try:
        LOCKFILE = zc.lockfile.LockFile('piLED')
    except zc.lockfile.LockError:
        issueCommand(args)
        exit(0)

    initializeGPIO(GPIODriver)
    LED = StatusLED(GPIODriver, Configuration)
    initializeRpc(LED)
    testLED(LED)
    setInitialStatus(LED)
    perpetualLoop()


def destruct(param1, param2):
    global LOCKFILE
    LOCKFILE.close()

def initializeGPIO(driver):
    driver.setmode(driver.BCM)
    driver.setwarnings(False)
    ledArray = Configuration.GPIO.Leds
    for led in ledArray:
        driver.setup(ledArray[led], driver.OUT, initial=driver.LOW)

def testLED(LED):
    for color in Colors.All:
        LED.setColor(color)
        sleep(0.15)

def setInitialStatus(LED):
    LED.enableBlink(0.2, Colors.Red, Colors.Black)

def initializeRpc(led):
    global PORT
    externalInterface = ExternalInterface(led)
    server = zerorpc.Server(externalInterface)
    URL = "tcp://0.0.0.0:" + str(PORT)
    server.bind(URL)
    server.run()


def perpetualLoop():
    while True:
        pass


def portInUse():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    inUse = False

    try:
        s.bind(("127.0.0.1", PORT))
    except socket.error as e:
        if e.errno == errno.EADDRINUSE:
            inUse = True

    s.close()
    return inUse

def issueCommand(args):
    pass



if __name__ == "__main__":
    main()
