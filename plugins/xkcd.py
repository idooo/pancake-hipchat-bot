import random
import requests

class XKCDPlugin():

    help = "Get random xkcd comics"
    command = "xkcd"

    @staticmethod
    def response():

        max_value = 1335
        value = random.randint(1, max_value)

        r = requests.get('http://xkcd.com/{}/info.0.json'.format(value))

        if r.status_code == 200:
            response = r.json()
            return [response['img'], response['alt']]

        else:
            return "Can't connect to xkcd API =("