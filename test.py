import zerorpc
from Data.Colors import Colors

c = zerorpc.Client()
c.connect("tcp://127.0.0.1:4242")
c.sequence(0.2, [Colors.Red, Colors.Green, Colors.Blue])
