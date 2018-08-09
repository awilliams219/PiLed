import os
import sys

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
    LED.sequence(Colors.All)

def initializeRpc(led):
    global PORT
    externalInterface = ExternalInterface(led)
    server = zerorpc.Server(externalInterface)
    URL = "ipc:///tmp/piled"
    server.bind(URL)
    server.run()


def perpetualLoop():
    while True:
        pass


def issueCommand(args):
    pass

def spawnDaemon(func):
    # do the UNIX double-fork magic, see Stevens' "Advanced
    # Programming in the UNIX Environment" for details (ISBN 0201563177)
    try:
        pid = os.fork()
        if pid > 0:
            # parent process, return and keep running
            return
    except OSError as e:
        print >>sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)

    os.setsid()

    # do second fork
    try:
        pid = os.fork()
        if pid > 0:
            # exit from second parent
            sys.exit(0)
    except OSError as e:
        print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)

    # do stuff
    func()

    # all done
    os._exit(os.EX_OK)

if __name__ == "__main__":
    spawnDaemon(main)
    


