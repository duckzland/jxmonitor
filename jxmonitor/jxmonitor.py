#!/usr/bin/env python
#####
# Main Miner Monitoring
#####

import sys, time, os, getopt, signal

# Registering main root path for sane building!
sys.path.append(os.path.dirname(__file__))

from threads.updater  import *
from modules.utility  import printLog
from entities.layout  import *
from entities.threads import *

def usage():
    print 'jxmonitor -s|-h|-v'
    print '   -s    Display the monitor in a single column'
    print '   -h    Prints this help message'
    print '   -v    Prints the jxmonitor version'

def version():
    print "0.3.3"

def main():

    global JobThreads
    global UpdaterThread
    global MainLayout

    # Setup tools dont allow argument
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv,"hi:si:vi")

    except getopt.GetoptError:
        usage()
        sys.exit(2)

    singleColumn = False
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()

        if opt == '-v':
            version()
            sys.exit()

        if opt == '-s':
            singleColumn = True

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    try:
        MainLayout = Layout(singleColumn)
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

    except Exception as e:
        printLog(str(e), 'error')
        status = 'error'

    finally:
        printLog("Closing interface", status)

    try:
        JobThreads.destroy()
        JobThreads.clean()
        status = 'success'

    except Exception as e:
        printLog(str(e), 'error')
        status = 'error'

    finally:
        printLog("Closing open threads", status)


if __name__ == "__main__":
    main()
