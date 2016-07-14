import re
import random
import inspect
import logging
from time import time, sleep
from urllib2 import HTTPError

from plugin_loader import PluginLoader
from simple_hipchat import HipChat

logger = logging.getLogger('pancake')

class Bot():

    rooms = None
    joined_rooms = {}
    actions = {}

    plugins = []

    # hipchat simple interaction object
    hipster = None
    name = 'Pancake'

    refresh_time = 6  # seconds

    rooms_users = {}
    get_users_timeout = 5 * 60 # 5 min

    def __init__(self, conf):

        api_token = conf['general']['api_token']
        name = conf['general']['bot_name']

        self.hipster = HipChat(token=api_token)

        try:
            self.available_rooms = dict(map(lambda x:[x['name'],x['room_id']], self.hipster.list_rooms()['rooms']))
        except HTTPError:
            logger.error('Error! API token not specified or invalid')
            exit()

        if name:
            self.name = name

        pl = PluginLoader(conf, '/plugins')

        self.plugins = pl.get_plugins()

        self.__set_actions()

    # Private
    # ==================================================================

    @staticmethod
    def __get_latest_date(messages):
        latest_date = ''
        for message in messages:
            if message['date'] > latest_date:
                latest_date = message['date']

        return latest_date

    @staticmethod
    def __mention_user(username):
        return '@' + username.replace(' ', '')

    def __set_actions(self):

        self.actions = {
            '/help': {
                'action': self.__cmd_help,
                'help': 'Show this help'
            },
            '/limit': {
                'action': self.__cmd_get_limit,
                'help': 'Get current HipChat API limit status'
            }
        }

        # load plugins
        for plugin in self.plugins:
            self.actions.update({
                '/' + plugin.command: {
                    'action': plugin.response,
                    'help': plugin.help
                }
            })

    def __get_messages(self, room_name, last_date):
        msgs = self.hipster.method(
            'rooms/history',
            method='GET',
            parameters={'room_id': self.joined_rooms[room_name], 'date': 'recent'}
        )['messages']

        new_messages = []
        for i in xrange(len(msgs), 0, -1):
            if msgs[i-1]['date'] > last_date:
                new_messages.append(msgs[i-1])

        return new_messages

    def __get_latest_dates(self):
        last_dates = {}
        for room_name in self.joined_rooms:
            msgs = self.hipster.method(
                'rooms/history',
                method='GET',
                parameters={'room_id': self.joined_rooms[room_name], 'date': 'recent'}
            )['messages']

            last_dates.update({room_name: self.__get_latest_date(msgs)})

        return last_dates

    def __get_users(self, room_name):
        if not room_name in self.rooms_users or self.rooms_users[room_name]['time'] + self.get_users_timeout < time():
            users = self.hipster.method(
                'rooms/show',
                method='GET',
                parameters={'room_id': self.joined_rooms[room_name]}
            )['room']['participants']

            self.rooms_users.update({room_name: {
                'users': users,
                'time': time()
            }})

        return self.rooms_users[room_name]['users']

    def __get_random_user(self, room_name):
        username = '@here'
        user = random.choice(self.__get_users(room_name))
        if user:
            username = self.__mention_user(user['name'])

        return username

    def __get_mentioned_user(self, room_name, message):
        message_parts = message.split()
        username = None

        search = message_parts[0]
        if len(message_parts) > 1:  # Full message, use second arg.
            search = message_parts[1]

        search = re.compile(search, re.IGNORECASE)

        users = self.__get_users(room_name)
        usernames = [user['name'] for user in users if re.search(search, user['name'])]
        if usernames:
            username = self.__mention_user(random.choice(usernames))

        return username

    # Commands
    # ==================================================================

    def __cmd_help(self):
        message = 'Pancake bot, here are available commands:\n'
        for action_name in self.actions.keys():
            message += action_name
            if 'help' in self.actions[action_name]:
                message += ' - ' + self.actions[action_name]['help']
            message += '\n'

        return message

    def __cmd_get_limit(self):
        message = '{0}/{1} calls remaining, update in {2} seconds'.format(
            self.hipster.limits['remaining'],
            self.hipster.limits['limit'],
            self.hipster.limits['reset'] - time()
        )

        return message

    # Public
    # ==================================================================

    def join_rooms(self, rooms):
        self.rooms = rooms.split(',')
        for room in self.rooms:
            self.join_room(room)

    def join_room(self, room_name):
        if room_name in self.available_rooms:
            self.joined_rooms.update({room_name: self.available_rooms[room_name]})

    def post_message(self, room_name, message):
        self.hipster.message_room(self.joined_rooms[room_name], self.name, message)

    def execute_action(self, action, room_name, message_object):
        args = {}
        fields = set(inspect.getargspec(action).args)

        if 'room' in fields: args.update({'room': room_name})
        if 'author_id' in fields: args.update({'author_id': message_object['from']['user_id']})
        if 'author' in fields: args.update({'author': self.__mention_user(message_object['from']['name'])})
        if 'message' in fields: args.update({'message': message_object['message']})
        if 'random_user' in fields: args.update({'random_user': self.__get_random_user(room_name)})
        if 'mentioned_user' in fields:
            args.update({'mentioned_user': self.__get_mentioned_user(room_name, message_object['message'])})

        messages = action(**args)

        if not isinstance(messages, list):
            messages = [messages]

        for message in messages:
            self.post_message(room_name, message)

    def start(self):
        last_dates = self.__get_latest_dates()
        while True:
            logger.debug('.')

            for room_name in self.joined_rooms:
                try:
                    messages = self.__get_messages(room_name, last_dates[room_name])

                    if messages:
                        last_dates[room_name] = self.__get_latest_date(messages)

                    for message in messages:
                        if message['from']['name'] == self.name: continue

                        for action_name in self.actions:
                            if action_name in message['message']:
                                logger.info("Executing action: " + action_name + " in room '" + room_name + "'")
                                self.execute_action(self.actions[action_name]['action'], room_name, message)

                except Exception, e:
                    logger.error(str(e))

            sleep(self.refresh_time)
