import requests
import re
import random
import inspect
from time import time
from ec2_helper import EC2Helper
from simple_hipchat import HipChat
from time import sleep
from urllib2 import HTTPError

# For Arnold
from _arnold_phrases import ARNOLD_PHRASES

class Bot():

    RE_URL = re.compile("<url>([^<]*)</url>", re.MULTILINE + re.IGNORECASE)
    EC2_DOWN_CODE = 80

    ec2 = None
    rooms = None
    joined_rooms = {}
    actions = {}

    # hipchat simple interaction object
    hipster = None
    name = 'Pancake'

    refresh_time = 6  # seconds

    rooms_users = {}
    get_users_timeout = 5 * 60 # 5 min

    def __init__(self, api_token, name=None, aws=False):

        self.hipster = HipChat(token=api_token)

        try:
            self.available_rooms = dict(map(lambda x:[x['name'],x['room_id']], self.hipster.list_rooms()['rooms']))
        except HTTPError:
            print('Error! API token not specified or invalid')
            exit()

        if aws:
            self.__awsInit(aws)

        if name:
            self.name = name

        self.__setActions()

    # Private
    # ==================================================================

    def __setActions(self):

        self.actions = {
            '/help': {
                'action': self.__cmdHelp,
                'help': 'Show this help'
            },
            '/cat': {
                'action': self.__cmdGetRandomCatGIF,
                'help': 'Post random cat gif'
            },
            '/staging': {
                'action': self.__cmdGetStagingStatus,
                'help': 'Get staging servers status'
            },
            '/chuck': {
                'action': self.__cmdGetRandomChuckPhrase,
                'help': 'Post random Chuck\'s phrase'
            },
            '/blame': {
                'action': self.__cmdBlameSomebody,
                'help': 'Blame somebody'
            },
            '/pony': {
                'action': self.__cmdGetPony,
                'help': 'Post pony image'
            },
            '/rps': {
                'action': self.__cmdRPS,
                'help': 'Rock - Paper - Scissors - Lizard - Spock (type /rps help)'
            },
            '/!': {
                'action': self.__cmdArnold,
                'help': 'Arnold Schwarzenegger\'s phrase (/! name)'
            },
            '/xkcd': {
                'action': self.__cmdXKCD,
                'help': 'Get random xkcd comics'
            },
            '/gif': {
                'action': self.__cmdRandomGIF,
                'help': 'Get a random gif, with a optional search term (/gif keyboard cat)'
            },
            '/roll': {
                'action': self.__cmdRoll,
                'help': 'Roll a random number 0 - 100'
            },
            '/limit': {
                'action': self.__cmdGetLimit,
                'help': 'Get current HipChat API limit status'
            },
            '/?': {
                'action': self.__cmdAsk,
                'help': 'Ask me a question'
            }
        }

    def __awsInit(self, credentials):
        if not ('secret_key' in credentials and 'access_key' in credentials):
            return False

        self.ec2 = EC2Helper(credentials['access_key'], credentials['secret_key'])

    def __getMessages(self, room_name, last_date):
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

    def __getLatestDate(self, messages):
        latest_date = ''
        for message in messages:
            if message['date'] > latest_date:
                latest_date = message['date']

        return latest_date

    def __getLatestDates(self):
        last_dates = {}
        for room_name in self.joined_rooms:
            msgs = self.hipster.method(
                'rooms/history',
                method='GET',
                parameters={'room_id': self.joined_rooms[room_name], 'date': 'recent'}
            )['messages']

            last_dates.update({room_name: self.__getLatestDate(msgs)})

        return last_dates

    def __getUsers(self, room_name):
        if not room_name in self.rooms_users or self.rooms_users[room_name]['time'] + self.get_users_timeout < time():
            users =  self.hipster.method(
                'rooms/show',
                method='GET',
                parameters={'room_id': self.joined_rooms[room_name]}
            )['room']['participants']

            self.rooms_users.update({room_name: {
                'users': users,
                'time': time()
            }})

        return self.rooms_users[room_name]['users']

    def __mentionUser(self, username):
        return '@' + username.replace(' ','')

    def __getRandomUser(self, room_name):
        username = '@here'
        user = random.choice(self.__getUsers(room_name))
        if user:
            username = self.__mentionUser(user['name'])

        return username

    def __getMentionedUser(self, room_name, message):
        message_parts = message.split()
        username = None

        if len(message_parts) > 1:
            # create regexp to find a user
            message_parts[1] = re.compile(message_parts[1], re.IGNORECASE)

            users = self.__getUsers(room_name)
            usernames = []
            for user in users:
                if re.search(message_parts[1], user['name']):
                    usernames.append(user['name'])

            if usernames:
                username = self.__mentionUser(random.choice(usernames))

        return username

    # Commands
    # ==================================================================

    def __cmdHelp(self, room_name):
        message = 'Pancake bot, here are available commands:\n'
        for action_name in self.actions.keys():
            message += action_name
            if 'help' in self.actions[action_name]:
                message += ' - ' + self.actions[action_name]['help']
            message += '\n'

        self.postMessage(room_name, message)

    def __cmdGetRandomChuckPhrase(self, room_name):
        message = "Can't connect to Chuck API =("
        params = {'limitTo': '[nerdy]'}

        r = requests.get('http://api.icndb.com/jokes/random', params=params)

        if r.status_code == 200:
            response = r.json()

            if response['type'] == 'success':
                message = response['value']['joke']

        self.postMessage(room_name, message)

    def __cmdGetRandomCatGIF(self, room_name):
        message = "Can't connect to cat API =("
        params = {'format': 'xml', 'type': 'gif'}

        r = requests.get('http://thecatapi.com/api/images/get', params=params)

        if r.status_code == 200:
            response = r.text

            res = re.search(self.RE_URL, response)
            if res:
                message = res.groups()[0]

        self.postMessage(room_name, message)

    def __cmdGetStagingStatus(self, room_name):

        if not self.ec2:
            self.postMessage(room_name, 'Can\'t connect to AWS API =(')
            return False

        is_up = False
        message = ''
        short_status = 'Staging servers status: '

        instances = self.ec2.getInstanceStatuses()
        for instance in instances:
            is_up = is_up or instance['state_code'] != self.EC2_DOWN_CODE
            message += instance['name'] + ': ' + instance['state'] + '\n'

        if is_up:
            short_status += 'RUNNING'
        else:
            short_status += 'STOPPED'

        self.postMessage(room_name, short_status)
        self.postMessage(room_name, message)

    def __cmdBlameSomebody(self, room_name):
        message = '{}, this is your fault!'
        username = self.__getRandomUser(room_name)

        self.postMessage(room_name, message.format(username))

    def __cmdGetPony(self, room_name):
        max = 160
        message = "http://ponyfac.es/{}/full.jpg".format(random.randint(1, max))
        self.postMessage(room_name, message)

    def __cmdRPS(self, room_name, username, message):

        if 'help' in message:
            self.postMessage(room_name, 'http://a.tgcdn.net/images/products/additional/large/db2e_lizard_spock.jpg')
            return False

        options = ['Rock', 'Paper', 'Scissors', 'Lizard', 'Spock']
        response = '{0} - {1}'.format(self.__mentionUser(username), random.choice(options))
        self.postMessage(room_name, response)

    def __cmdAsk(self, room_name, username):
        options = ['yes', 'no', 'no way!', 'yep!']
        response = '{0}, {1}'.format(self.__mentionUser(username), random.choice(options))
        self.postMessage(room_name, response)

    def __cmdArnold(self, room_name, message):
        phrase = random.choice(ARNOLD_PHRASES)

        # try to get mentioned username
        username = self.__getMentionedUser(room_name, message)

        # if not - we will get random username
        if not username:
            username = self.__getRandomUser(room_name)

        self.postMessage(room_name, phrase.format(username))

    def __cmdXKCD(self, room_name):
        max_value = 1335
        value = random.randint(1, max_value)

        r = requests.get('http://xkcd.com/{}/info.0.json'.format(value))

        if r.status_code == 200:
            response = r.json()
            self.postMessage(room_name, response['img'])
            self.postMessage(room_name, response['alt'])

        else:
            self.postMessage(room_name, "Can't connect to xkcd API =(")

    def __cmdRandomGIF(self, room_name, message):
        search_values = message.split('/gif', 1)
        tags = ''
        if len(search_values) == 2:
            tags = '+'.join(search_values[1].split())
        r = requests.get('http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag=' + tags)

        if r.status_code == 200:
            response = r.json()
            self.postMessage(room_name, response['data']['image_url'])

        else:
            self.postMessage(room_name, "Can't connect to giphy API =(")

    def __cmdRoll(self, room_name, username):
        response = '{0} rolled {1}'.format(self.__mentionUser(username), random.randint(0, 100))
        self.postMessage(room_name, response)

    def __cmdGetLimit(self, room_name):
        message = '{0}/{1} calls remaining, update in {2} seconds'.format(
            self.hipster.limits['remaining'],
            self.hipster.limits['limit'],
            self.hipster.limits['reset'] - time()
        )
        self.postMessage(room_name, message)

    # Public
    # ==================================================================

    def joinRooms(self, rooms):
        self.rooms = rooms.split(',')
        for room in self.rooms:
            self.joinRoom(room)

    def joinRoom(self, room_name):
        if room_name in self.available_rooms:
            self.joined_rooms.update({room_name: self.available_rooms[room_name]})

    def postMessage(self, room_name, message):
        self.hipster.message_room(self.joined_rooms[room_name], self.name, message)

    def start(self):

        last_dates = self.__getLatestDates()

        while True:

            print('.')

            for room_name in self.joined_rooms:
                
                try:
                    messages = self.__getMessages(room_name, last_dates[room_name])

                    if messages:
                        last_dates[room_name] = self.__getLatestDate(messages)

                    for message in messages:

                        if message['from']['name'] != self.name:

                            for action_name in self.actions:

                                fields = set(inspect.getargspec(self.actions[action_name]['action'])[0])
                                args = {'room_name': room_name}

                                if 'user_id' in fields:
                                    args.update({'user_id': message['from']['user_id']})

                                if 'username' in fields:
                                    args.update({'username': message['from']['name']})

                                if 'message' in fields:
                                    args.update({'message': message['message']})

                                if action_name in message['message']:
                                    self.actions[action_name]['action'](**args)

                except Exception, e:
                    print(str(e))

            sleep(self.refresh_time)
