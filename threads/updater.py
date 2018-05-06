import sys, pickle, io, select, time, socket, json
sys.path.append('../')
from entities.job import *
from thread import Thread
from modules.transfer import *
from modules.utility import printLog

class Updater(Thread):

    def __init__(self, Layout):
        self.host = "127.0.0.1"
        self.port = 8129
        self.active = False
        self.job = False
        self.transfer = False
        self.connection = False
        self.layout = Layout
        self.buffers = ''
        self.init()
        self.start()


    def init(self):
        self.job = Job(0.2, self.update)
        self.active = True


    def update(self, runner):
        if self.active:
            try:
                if self.connection == False:
                    host = "127.0.0.1"
                    port = 8129
                    self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.connection.connect((self.host, self.port))

                if self.transfer == False:
                    if self.connection != False:
                        self.transfer = Transfer(self.connection)
                        self.transfer.send('getStatus')

                self.buffers = ''
                if self.transfer != False:
                    packet = self.transfer.recv()
                    if not packet:
                        raise
                    self.buffers = packet

                if self.layout.viewReady:
                    self.layout.view.update(self.buffers)

                if self.layout.loopReady:
                    self.layout.loop.draw_screen()

            except:
                self.connection = False
                self.transfer = False
                if self.layout.viewReady:
                    self.layout.view.update('')

                if self.layout.loopReady:
                    self.layout.loop.draw_screen()
                time.sleep(10)


    def stop(self, force = False):
        try:
            if self.transfer != False:
                self.transfer.send('close')
                self.transfer.wait()
                self.transfer.close()
                self.transfer = False

            if self.connection != False:
                #self.connection.close()
                self.connection.shutdown(socket.SHUT_WR)
                self.connection = False
        except:
            pass


    def destroy(self):
        try:
            if self.job:
                self.job.shutdown_flag.set()
            self.stop()
            self.active = False
            status = 'success'

        except:
            status = 'error'

        finally:
            self.active = False
            printLog("Stopping active thread", status)


    def extract(self):
        return self.buffers