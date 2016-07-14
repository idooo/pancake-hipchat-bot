#!/usr/bin/env python

__project_name__ = 'Pancake chat bot (HipChat edition)'
__version__ = '2.2.1'

import sys
import os
import logging
import argparse
import src as library

class PancakeDaemon(library.Daemon):

    def run(self):
        logger = logging.getLogger('pancake')
        logger.info(__project_name__ + ', version ' + __version__)
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
    parser.add_argument('-o', '--out',
        help='file to redirect output')
    parser.add_argument('operation',
        metavar='OPERATION',
        type=str,
        help='Operation with daemon. Accepts any of these values: start, stop, restart, status',
        choices=['start', 'stop', 'restart', 'foreground'])

    args = parser.parse_args()

    # Logging setup
    if args.out:
        handler = logging.FileHandler(args.out)
    else:
        handler = logging.StreamHandler()

    logger = logging.getLogger('pancake')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Config to use
    conf_name = args.config
    settings = library.config.Settings(conf_name)

    # Lockfile
    lockfile = args.pid
    pancakeDaemon = PancakeDaemon(lockfile)
    
    if args.operation == 'foreground':
        logger.info("Starting Pancake in foreground")
        pancakeDaemon.run()

    elif args.operation == 'start':
        logger.info("Starting Pancake")
        pancakeDaemon.start()

    elif args.operation == 'stop':
        logger.info("Stoping Pancake")
        pancakeDaemon.stop()

    elif args.operation == 'restart':
        logger.info("Restarting Pancake")
        pancakeDaemon.restart()

    sys.exit(0)
