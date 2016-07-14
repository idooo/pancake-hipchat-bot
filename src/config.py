# -*- coding: UTF-8 -*-

import ConfigParser
import os
import inspect
import logging


class Settings():

    __default_conf_name = 'example.conf'
    __conf = {}

    def __init__(self, filename=False):
        """
            Create config object, read config data from file and make
            friendly format ot access to config data
        """

        self.APP_DIR = os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]) + '/../'

        if not filename:
            filename = self.APP_DIR + 'conf/' + self.__default_conf_name

        self.CONF_NAME = filename

        config = ConfigParser.ConfigParser()
        config.readfp(open(filename))

        for section_name in config.sections():
            data = {}
            for item in config.items(section_name):
                try:
                    data.update({item[0]: str(config.get(section_name, item[0])).strip()})
                except ConfigParser.NoOptionError:
                    data.update({item[0]: None})

                if data[item[0]].lower() == 'false':
                    data[item[0]] = False

            self.__conf.update({
                section_name: data
            })

    def get(self, key=None):
        if not key: return self.__conf

        try:
            section, option = key.split(':')
            return self.__conf[section][option]
        except KeyError, e:
            raise Exception("Can't find config key in file: " + str(e))

