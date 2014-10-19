import requests
import json

class GeckoboardPlugin():

    help = "Post message to Geckoboard"
    command = "board"

    widget_key = None
    api_key = None

    def __init__(self, conf):
        if not 'geckoboard' in conf:
            raise Exception("There is no [geckoboard] section in the config file")

        if not 'api' in conf['geckoboard'] or not 'widget' in conf['geckoboard']:
            raise Exception("You must specify 'widget' and 'api' options "
                            "in [geckoboard] section in the config file")

        self.widget_key = conf['geckoboard']['widget']
        self.api_key = conf['geckoboard']['api']

    def response(self, message):

        message_parts = message.split(' ', 1)

        params = {
            "api_key": self.api_key,
            "data": {
                "item": [
                    { "text": message_parts[1], "type":0 }
                ]
            }
        }

        headers = {'Content-type': 'application/json'}
        r = requests.post('https://push.geckoboard.com/v1/send/' + self.widget_key,
                          data=json.dumps(params), headers=headers)

        if r.status_code == 200:
            response = r.json()

            if response['success']:
                return 'Message was posted to Geckoboard'

        return 'Something went wrong'