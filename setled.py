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
        if not hasattr(Colors, getColorName(color)):
            print(color + " is not a valid color")
            exit(2)


def getSequenceList(colors):
    runningList = list()
    for color in colors:
        runningList.append(getattr(Colors, getColorName(color)))
    return runningList


def configureArguments():
    global argParser
    argParser = argparse.ArgumentParser('setled', formatter_class=argparse.RawDescriptionHelpFormatter, epilog="Simpler options take precedence: Color > Blink > Sequence\n\nAvailable Colors:\n" + ', '.join(Colors.NamedAll.keys()))
    argParser.add_argument('--port', help='Specify HTTP port of LED daemon listener (default 4242)',
                           type=int, default=4242)
    argParser.add_argument('--interval', help='Time between color changes in seconds (default: 0.5).',
                           type=float, default=0.5)
    argParser.add_argument('--color', help='Set LED to static color', dest="static", type=str)
    argParser.add_argument('--blink', help='Alternate between two colors', dest='blink_color', nargs=2)
    argParser.add_argument('--sequence', help='Show unlimited number of colors in a repeating sequence',
                           nargs="*", dest='seq_color')
    argParser.add_argument('--off', help='Shut off the LED entirely', action='store_true')
    argParser.add_argument('color', help='Set LED to static color (same as --color)', nargs="?", type=str)
    return argParser.parse_args()

def getColorName(color):
    return color.title();

def nullEnd():
    print("No action specified.  Nothing to do.")
    exit(1)

args = configureArguments()

LED = initRPC(args.port)
interval = args.interval

staticColor = None
if args.static is not None:
    staticColor = getColorName(args.static)
if args.color is not None:
    staticColor = getColorName(args.color)

if args.off:
    LED.setColor(Colors.Off)
    exit(0)

if staticColor is not None:
    validateColors([staticColor])
    LED.setColor(getattr(Colors, staticColor))
    exit(0)

if args.blink_color is not None:
    validateColors(args.blink_color)
    LED.blink(interval, getattr(Colors,
                                getColorName(args.blink_color[0])), getattr(Colors, getColorName(args.blink_color[1])))
    exit(0)

if args.seq_color is not None:
    validateColors(args.seq_color)
    LED.sequence(interval, getSequenceList(args.seq_color))
    exit(0)

nullEnd()

