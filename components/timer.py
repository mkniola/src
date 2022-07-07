from threading import Thread, Event
import time


class StoppableThread(Thread):
    """Stoppable thread."""

    def __init__(self):
        """Init."""
        Thread.__init__(self)
        self.stop_event = Event()        

    def stop(self):
        """Stop."""
        if self.isAlive() is True:
            # set event to signal thread to terminate
            self.stop_event.set()
            # block calling thread until thread really has terminated
            self.join()


class IntervalTimer(StoppableThread):

    def __init__(self, interval, worker_func):
        super().__init__()
        self._interval = interval
        self._worker_func = worker_func

    def run(self):
        while not self.stop_event.is_set():
            self._worker_func()
            time.sleep(self._interval)