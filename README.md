PiLed
-------
Helpful RGB LED driver for Raspberry Pi

### Why?

When working on my project, I realized there wasn't really a good ready-made solution to manipulating 
GPIO pins to work an LED.  It occurred to me that this is probably a fairly common use case that 
requires frequent "reinventing of the wheel" for people working on PI projects.  So, I broke the LED 
management section out of my project into its own service, and thus PiLed was born.

### Installation

1. Clone the repo wherever you want.  I use /opt/piled, but it's your Pi, so don't feel like you have 
to do it my way.
2. Install the dependencies in requirements.txt using PIP3.
3. Add the PiLed daemon to your Pi's startup scripts somewhere.  You could add it to /etc/rc.local, 
or, if you're feeling froggy, add it to your init config.  Maybe make an upstart job?  Dunno.  It's your 
world.  Make sure to fork the process when you start it since the daemon doesn't currently self-fork.
(Hint: you can do this in your rc.local by adding `python3 /opt/piled/ &` to the bottom of the file.  
Obvs, adjust the path to wherever you put PiLed when you cloned it.)
4. The PiLed daemon defaults to listening on port 4242.  If you need to change this, you can do so at the 
top of \_\_main\_\_.py.  Just sub in whatever port you want to use instead.
5. Either reboot or start the daemon manually by running `python3 /opt/piled/ &` (adjust path as needed).


### Hardware and Wiring

PiLed assumes your RGB LED is connected to PINS 16, 20, and 21, and that you have your LED wired to 
power on in a digital HIGH state.  I recommend using a common-cathode LED with the cathode connected to
GND.  **Don't forget those current-limiting resistors unless you want to burn out the GPIO ports.**

If you need to change the GPIO pin assignments, you can do so near the top of \_\_main\_\_.py in the 
`Pins` list.  Just change the assignments to the GPIO pin numbers you are using for your LED.  **Be sure 
to use the GPIO number, NOT the header or pin number.**  If you don't know what this means, google it before 
proceeding because it's important.  

### Usage

There are two ways to use PiLed:  You can either use it via the command line by calling setled.py, or you 
can interact with it using the RPC api.  I'll detail both methods below.

##### Command-line tool

The command line tool is available at /opt/piled/setled.py.  I'd recommend creating an alias for this in your
.bashrc file, but you do you.

Before beginning, be sure to `chmod +x /opt/piled/setled.py` or you're not going to get very far.

###### Command-line options:

>setled [-h] [--port PORT] [--interval SECONDS] [--color STATIC]
              [--blink COLOR COLOR] [--sequence [COLOR [COLOR ...]]] [--off]
              [color]


`-h` will display usage information

`--port` allows you to override the port that the RPC service is running on.  This defaults to 4242, but if 
you've changed the port on the service, you'll need to override that here.

`--interval SECONDS` Allows you to change the timing of the blink and sequence options.  This has no effect
on the static color setting

`--color STATIC` Allows you to set the led to a static color.  

`--blink COLOR COLOR` Allows you to alternate between to static colors.  Timing defaults to 0.5 seconds, 
but you can override this with the `--interval` option.

`--sequence COLOR [COLOR ...]` Allows you to set a preprogrammed sequence that will repeat.  There is 
no limit to the number of colors in the sequence beside normal limits on commandline length.  Colors will 
advance through the sequence every 0.5 seconds, or at whatever interval you've specified with `--interval`.

`[color]` Can be used to specify a static color.  This is the same as specifying `--color`.

Available colors are: Red, Blue, Green, Magenta, Yellow, Cyan, and White.  PiLed does not currently support
PWM output, so colors are limited to these options.  Additionally, you can specify Black or Off to turn 
the LED off entirely.

##### RPC Service

PiLed exposes an RPC interface on a local TCP/IP port (default is 4242).  You can hook into that service
in your own project to manipulate the LED directly without going through the commandline tool.  This 
has the advantage of not only being simpler, but also faster, as the commandline tool has to connect to
the RPC service at every execution whereas your application can leave the connection open and eliminate 
that overhead.

To hook into the service, use PIP to install `zerorpc` into your project.  Add the following code to 
your project somewhere.  This should only run once, then the LED object should be passed around via dependency injection
or via a global variable (eww).  If you've changed the port that the PiLed daemon runs on, remember to 
change 4242 below to match the new port. 
``` 
    LED = zerorpc.Client()
    LED.connect("tcp://127.0.0.1:4242"))
```

###### RPC Usage

The LED object will have the following methods available on it:

`LED.getColors()` returns a dictionary containing all of the available colors.  Use these color 
definitions in other methods below.

`LED.setColor(color)` sets the LED to a static color.  

`LED.blink(interval, color1, color2)` alternates the LED between two colors every _interval_ seconds. Fractions of a second are perfectly acceptable.

`LED.sequence(interval, colors)` allows you to specify a repeating sequence of led colors with each color appearing for _interval_ seconds.  _colors_ is a list or tuple containing your color sequence in order.

`LED.off()` turns off the LED entirely.  This is the same as setting the color to Black or Off.

#### Contributing

Want to add something?  Tweak something?  Fork the project, make your changes, then shoot me a pull request.  

#### License

PiLed is released under GPLv3. 