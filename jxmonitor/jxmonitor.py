#!/usr/bin/env python
#####
# Main Miner Monitoring
#####

import sys, time, os

from threads.updater import *
from modules.utility import printLog
from entities.layout import *
from entities.threads import *


def main():

    global JobThreads
    global UpdaterThread
    global MainLayout

    try:
        MainLayout = Layout()
        JobThreads = Threads()
        JobThreads.add('updater', Updater(MainLayout))

        MainLayout.init()
        MainLayout.main()

        # Keep the main thread running, otherwise signals are ignored.
        while True:
            time.sleep(1)

    except:
        shutdown()

    finally:
        printLog('Exiting monitoring program', 'success')
        os._exit(1)

def shutdown():

    try:
        MainLayout.destroy()
        status = 'success'
    except:
        status = 'error'
    finally:
        printLog("Closing interface", status)

    try:
        JobThreads.destroy()
        JobThreads.clean()
        status = 'success'
    except:
        status = 'error'
    finally:
        printLog("Closing open threads", status)


if __name__ == "__main__":
    main()
