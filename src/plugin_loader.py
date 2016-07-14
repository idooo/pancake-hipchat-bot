import os
import sys
import inspect
import logging

logger = logging.getLogger('pancake')


class PluginLoader():

    __plugins = []
    __plugin_names = {}

    conf = None
    app_dir = os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]) + '/../'

    def __init__(self, conf, plugins_dir):
        self.conf = conf
        folder = self.app_dir + plugins_dir

        sys.path.insert(0, folder)

        for filename in os.listdir(folder):
            full_path = folder + '/' + filename

            if os.path.isdir(full_path) or filename[-3:] == '.py':
                self.load_plugin(filename)

    def __check_conflicts(self, command):
        for plugin in self.__plugins:
            if command == plugin.command:
                raise Exception("Command name '" + command + "' conflicts with plugin: " + self.__plugin_names[plugin.command])

    def get_plugins(self):
        return self.__plugins

    def load_plugin(self, filename):
        """
            Load plugin class, check if it has all the required properties
            and initialise it
        """

        try:

            if filename[-2:] == 'py':
                filename = filename[:-3:]

            __import__(filename)

            for name, class_name in inspect.getmembers(sys.modules[filename]):
                if inspect.isclass(class_name):
                    args = {}

                    if hasattr(class_name, '__init__') and 'conf' in inspect.getargspec(class_name.__init__).args:
                        args.update({'conf': self.conf})

                    plugin = class_name(**args)
                    if not hasattr(plugin, 'help') or not hasattr(plugin, 'command') or len(plugin.command) == 0:
                        raise Exception("Plugin class must have 'help' and 'command' attributes")

                    self.__check_conflicts(plugin.command)

                    self.__plugins.append(plugin)
                    self.__plugin_names.update({plugin.command: filename})

                    logger.info("Plugin '" + filename + "' (/" + plugin.command + ") was loaded...")

                    return True

            raise Exception("No class found in " + filename)

        except Exception, e:
            logger.warning("Can't load plugin '" + filename + "': " + str(e))


