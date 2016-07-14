#!/usr/bin/env python

__project_name__ = 'Pancake chat bot (HipChat edition)'
__version__ = '2.2.0'

from daemon import Daemon
import sys
import os
import argparse
import src as library

class PancakeDaemon(Daemon):

    def run(self):
        print(__project_name__ + ', version ' + __version__)
        bot = library.Bot(settings.get())
        bot.join_rooms(settings.get('general:rooms'))
        bot.start()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config',
        help='config file to be used')
    parser.add_argument('-p', '--pid', 
        default=os.path.dirname(os.path.realpath(__file__)) + '/pancake.pid', 
        help='pecify path for pid file')
    parser.add_argument('operation',
        metavar='OPERATION',
        type=str,
        help='Operation with daemon. Accepts any of these values: start, stop, restart, status',
        choices=['start', 'stop', 'restart', 'foreground'])

    args = parser.parse_args()

    # Config to use
    conf_name = args.config
    settings = library.config.Settings(conf_name)

    # Lockfile
    lockfile = args.pid
    pancakeDaemon = PancakeDaemon(lockfile)
    
    if args.operation == 'foreground':
        pancakeDaemon.run()

    elif args.operation == 'start':
        print("Starting Pancake")
        pancakeDaemon.start()

    elif args.operation == 'stop':
        print("Stoping Pancake")
        pancakeDaemon.stop()

    elif args.operation == 'restart':
        print("Restarting Pancake")
        pancakeDaemon.restart()

    elif args.operation == 'status':
        print("Viewing Pancake status")

    sys.exit(0)
