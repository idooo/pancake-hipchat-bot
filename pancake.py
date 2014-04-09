#!/usr/bin/env python

import argparse
import src as library

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='config file to be used')

    args = parser.parse_args()

    # Config to use
    conf_name = args.config
    conf = library.config.Settings(conf_name)

    bot = library.Bot(
        conf.credentials['url'],
        conf.credentials['api'],
        aws=conf.aws
    )
    bot.joinRooms(conf.credentials['room'])
    bot.start()
