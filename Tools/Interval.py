from threading import Timer


class Interval:
    def __init__(self, interval, callback, *callbackParams):
        self.abort = False
        self.timer = Timer(interval, lambda: callback(*callbackParams))
        self.timer.start()

    def cancel(self):
        self.abort = True
        self.timer.cancel()
