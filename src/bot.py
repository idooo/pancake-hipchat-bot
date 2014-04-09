import requests
import re
import random
import inspect
import hipchat
from ec2_helper import EC2Helper
from time import sleep

# For Arnold
from _arnold_phrases import ARNOLD_PHRASES

class Bot():

    RE_URL = re.compile("<url>([^<]*)</url>", re.MULTILINE + re.IGNORECASE)
    EC2_DOWN_CODE = 80

    ec2 = None
    rooms = None
    joined_rooms = {}
    actions = {}
    user = {}

    _users = {}

    def __init__(self, url, api_key, rooms=False, aws=False):

        self.url = url
        self.api_key = api_key

        request = Request(url, api_key)
        self.campfire = Campfire(request)

        self.account = self.campfire.account()
        self.available_rooms = self.campfire.rooms()

        self.user = self.campfire.user()

        if rooms:
            self.joinRooms(rooms)

        if aws:
            self.__awsInit(aws)

        self.__setActions()

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
            '/?': {
                'action': self.__cmdAsk,
                'help': 'Ask me a question'
            }
        }

    def __awsInit(self, credentials):
        if not ('secret_key' in credentials and 'access_key' in credentials):
            return False

        self.ec2 = EC2Helper(credentials['access_key'], credentials['secret_key'])

    def __getMessages(self, messages, last_id):
        new_messages = [];
        for i in xrange(len(messages), 0, -1):
            if messages[i-1]['id'] > last_id:
                new_messages.append(messages[i-1])

        return new_messages

    def __getUser(self, room, user_id):

        if str(user_id) in self._users:
            return self._users[str(user_id)]
        else:
            users = room.status()['users']
            for user in users:
                self._users[str(user['id'])] = user['name']

            if str(user_id) in self._users:
                return self._users[str(user_id)]

        return 'Unknown'

    def __getRandomUser(self, room):
        users = room.status()['users']
        usernames = []
        for user in users:
            if user['name'] != self.user['name']:
                usernames.append(user['name'])

        return random.choice(usernames)

    def __getMentionedUser(self, room, message):
        message_parts = message.split()
        username = None

        if len(message_parts) > 1:
            # create regexp to find a user
            message_parts[1] = re.compile(message_parts[1], re.IGNORECASE)

            users = room.status()['users']
            usernames = []
            for user in users:
                if user['name'] != self.user['name'] and re.search(message_parts[1], user['name']):
                    usernames.append(user['name'])

            if usernames:
                username = random.choice(usernames)

        return username

    def __cmdHelp(self, room):
        message = 'Pancake bot, here are available commands:\n'
        for action_name in self.actions.keys():
            message += action_name
            if 'help' in self.actions[action_name]:
                message += ' - ' + self.actions[action_name]['help']
            message += '\n'

        room.speak(message)

    def __cmdGetRandomChuckPhrase(self, room):
        message = "Can't connect to Chuck API =("
        params = {'limitTo': '[nerdy]'}

        r = requests.get('http://api.icndb.com/jokes/random', params=params)

        if r.status_code == 200:
            response = r.json()

            if response['type'] == 'success':
                message = response['value']['joke']

        room.speak(message)

    def __cmdGetRandomCatGIF(self, room):
        message = "Can't connect to cat API =("
        params = {'format': 'xml', 'type': 'gif'}

        r = requests.get('http://thecatapi.com/api/images/get', params=params)

        if r.status_code == 200:
            response = r.text

            res = re.search(self.RE_URL, response)
            if res:
                message = res.groups()[0]

        room.speak(message)

    def __cmdGetStagingStatus(self, room):

        if not self.ec2:
            room.speak('Can\'t connect to AWS API =(')
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

        room.speak(short_status)
        room.speak(message)

    def __cmdBlameSomebody(self, room):
        message = '{}, this is your fault!'
        username = self.__getRandomUser(room)

        room.speak(message.format(username))

    def __cmdGetPony(self, room):
        max = 160
        message = "http://ponyfac.es/{}/full.jpg".format(random.randint(1, max))
        room.speak(message)

    def __cmdRPS(self, room, user_id, message):

        if 'help' in message:
            room.speak('Rock (:punch:), Paper (:hand:), Scissors (:v:), Lizard (:dragon:), Spock (:boy:)')
            room.speak('http://a.tgcdn.net/images/products/additional/large/db2e_lizard_spock.jpg')
            return False

        username = self.__getUser(room, user_id)
        options = [':hand:', ':v:', ':punch:', ':dragon:', ':boy: - (spock)']
        response = '{0} - {1}'.format(username, random.choice(options))
        room.speak(response)

    def __cmdAsk(self, room, user_id):
        username = self.__getUser(room, user_id)
        options = ['yes', 'no', 'no way!', 'yep!']
        response = '{0}, {1}'.format(username, random.choice(options))
        room.speak(response)

    def __cmdArnold(self, room, message):
        phrase = random.choice(ARNOLD_PHRASES)

        # try to get mentioned username
        username = self.__getMentionedUser(room, message)

        # if not - we will get random username
        if not username:
            username = self.__getRandomUser(room)

        room.speak(phrase.format(username))

    def __cmdXKCD(self, room):
        max_value = 1335
        value = random.randint(1, max_value)

        r = requests.get('http://xkcd.com/{}/info.0.json'.format(value))

        if r.status_code == 200:
            response = r.json()
            room.speak(response['img'])
            room.speak(response['alt'])

        else:
            room.speak("Can't connect to xkcd API =(")

    def __cmdRandomGIF(self, room, message):
        search_values = message.split('/gif', 1)
        tags = ''
        if len(search_values) == 2:
            tags = '+'.join(search_values[1].split())
        r = requests.get('http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag=' + tags)

        if r.status_code == 200:
            response = r.json()
            room.speak(response['data']['image_url'])

        else:
            room.speak("Can't connect to giphy API =(")

    def joinRooms(self, rooms):
        self.rooms = rooms.split(',')
        for room in self.rooms:
            self.joinRoom(room)

    def joinRoom(self, room):
        self.joined_rooms.update({room: self.campfire.room(room)})
        self.joined_rooms[room].join()

    def start(self):

        last_ids = {}
        for room_name in self.joined_rooms:
            msgs = self.joined_rooms[room_name].recent()
            last_ids.update({room_name: msgs[-1]['id']})

        while True:

            print '.'

            for room in self.joined_rooms:
                
                try:
                    msgs = self.joined_rooms[room].recent()

                    messages = self.__getMessages(msgs, last_ids[room])

                    if messages:
                        last_ids[room] = msgs[-1]['id']

                    command = None
                    for message in messages:

                        if message['body'] and message['user_id'] != self.user['id']:
                            for action_name in self.actions:

                                fields = set(inspect.getargspec(self.actions[action_name]['action'])[0])
                                args = {'room': self.joined_rooms[room]}

                                if 'user_id' in fields:
                                    args.update({'user_id': message['user_id']})

                                if 'message' in fields:
                                    args.update({'message': message['body']})

                                if action_name in message['body']:
                                    self.actions[action_name]['action'](**args)

                    if command:
                        print 'command', command

                except Exception, e:
                    print str(e)

            sleep(2)
