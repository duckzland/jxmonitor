import os, time, sys, threading, signal
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from modules.utility import printLog
from entities.shutdown import *

class Job(threading.Thread):

    """
        This is a class for defining a single Job instance
    """

    def __init__(self, ticks, func, *args):
        threading.Thread.__init__(self)
        self.ticks = ticks
        self.function = func
        self.args = args
        self.shutdown_flag = threading.Event()

    def run(self):
        while not self.shutdown_flag.is_set():
            self.function(self, *self.args)
            for i in range(int(self.ticks)):
                if not self.shutdown_flag.is_set():
                    time.sleep(1)