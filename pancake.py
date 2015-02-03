#!/usr/bin/env python

__project_name__ = 'Pancake chat bot (HipChat edition)'
__version__ = '2.1.0'

import argparse
import src as library

if __name__ == "__main__":

    print(__project_name__ + ', version ' + __version__)

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='config file to be used')

    args = parser.parse_args()

    # Config to use
    conf_name = args.config
    settings = library.config.Settings(conf_name)

    bot = library.Bot(settings.get())

    bot.join_rooms(settings.get('general:rooms'))
    bot.start()
