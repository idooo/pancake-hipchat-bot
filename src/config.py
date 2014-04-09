# -*- coding: UTF-8 -*-

import ConfigParser
import os
import inspect


class Settings():

    rules = {
        'credentials': ['api', 'url', 'room'],
        'aws': ['access_key', 'secret_key']
    }

    default_conf_name = 'example.conf'

    def __init__(self, filename=False):
        """
            Create config object, read config data from file and make
            friendly format ot access to config data
        """

        self.APP_DIR = os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]) + '/../'

        self.CONF_DIR = self.APP_DIR + 'conf/'

        if not filename:
            filename = self.default_conf_name
            self.FILENAME = self.CONF_DIR + filename

        self.CONF_NAME = filename

        config = ConfigParser.ConfigParser()
        config.readfp(open(self.CONF_DIR + filename))

        for section in self.rules.keys():
            data = {}
            for item in self.rules[section]:
                try:
                    data.update({item: str(config.get(section, item)).strip()})
                except ConfigParser.NoOptionError:
                    data.update({item: ''})
                except ConfigParser.NoSectionError:
                    for option in self.rules[section]:
                        data.update({option: False})
                    break

                if data[item].lower() == 'false':
                    data[item] = False

            setattr(self, section, data)
