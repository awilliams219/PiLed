#! /usr/bin/env python3
import zerorpc
import argparse
from Data.Colors import Colors



def initRPC(port):
    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:" + str(port))
    return c


def validateColors(colorsToValidate):
    for color in colorsToValidate:
        if not hasattr(Colors, color):
            print(color + " is not a valid color")
            exit(2)


def getSequenceList(colors):
    runningList = list()
    for color in colors:
        runningList.append(getattr(Colors, color))
    return runningList


argParser = argparse.ArgumentParser('setled', epilog="Available Colors:\n\n" + ', '.join(Colors.NamedAll.keys()))
argParser.add_argument('--port', help='Specify port of LED daemon listener (default 4242)',
                       type=int, default=4242)
argParser.add_argument('--interval', help='Time between color changes (default 0.5 seconds).',
                       type=float, default=0.5)
argParser.add_argument('--color',  help='Set LED to static color', type=str)
argParser.add_argument('--blink', help='Alternate between two colors', dest='blink_color', nargs=2)
argParser.add_argument('--sequence', help='Show unlimited number of colors in a repeating sequence',
                       nargs="*", dest='seq_color')
argParser.add_argument('--off', help='Shut off the LED entirely', action='store_true')

args = argParser.parse_args()

LED = initRPC(args.port)
interval = args.interval

if args.off:
    LED.setColor(Colors.Off)
    exit(0)

if args.color is not None:
    validateColors([args.color])
    LED.setColor(getattr(Colors, args.color))
    exit(0)

if args.blink_color is not None:
    validateColors(args.blink_color)
    LED.blink(interval, getattr(Colors, args.blink_color[0]), getattr(Colors, args.blink_color[1]))
    exit(0)

if args.seq_color is not None:
    validateColors(args.seq_color)
    LED.sequence(interval, getSequenceList(args.seq_color))
    exit(0)

print("No action specified.  Nothing to do.")
exit(1)

