
# Colors in format (Red, Green, Blue)
# States are binary on/off format
# LED Driver does not currently support analog values


class Colors:

    # Bitwise switches
    Black = 0
    Red = 1
    Green = 2
    Blue = 4

    White = Red + Green + Blue
    Yellow = Red + Green
    Magenta = Red + Blue
    Cyan = Green + Blue

    Off = Black

    Bright = (White, Yellow, Red, Magenta, Green, Cyan, Blue)
    All = (*Bright, Black)

    NamedAll = {"White": White, "Yellow": Yellow, "Red": Red, "Magenta": Magenta, "Green": Green,
                "Cyan": Cyan, "Blue": Blue, "Black": Black, "Off": Off}
