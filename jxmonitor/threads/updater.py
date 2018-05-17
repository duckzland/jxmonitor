import os, sys, pickle, io, select, time, socket, json
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
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
        self.active = True
        self.job = Job(1, self.update)


    def update(self, runner):
        retries = 3
        try:
            self.transfer.send('serverStatus')
        except:
            self.connection = False
            self.transfer = False
        finally:
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
                            if retries > 0:
                                time.sleep(1)
                                retries = retries - 1
                            else:
                                raise

                        self.buffers = packet

                    self.updateLayout(self.buffers)

                except:
                    self.connection = False
                    self.transfer = False
                    self.updateLayout('')
                    time.sleep(10)



    def updateLayout(self, content):
        try:
            if self.layout.viewReady:
                self.layout.view.update(content)

            if self.layout.loopReady:
                self.layout.loop.draw_screen()
        except:
            pass



    def stop(self, force = False):
        if self.active:
            try:
                if self.transfer != False:
                    self.transfer.send('close')
                    self.transfer = False

                if self.connection != False:
                    #self.connection.close()
                    self.connection.shutdown(socket.SHUT_WR)
                    self.connection = False
            except:
                pass


    def destroy(self):
        if self.active:
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