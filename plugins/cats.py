import re
import requests

class CatGIFPlugin():

    help = "Post a random cat gif"
    command = "cat"

    def __init__(self):
        self.RE_URL = re.compile("<url>([^<]*)</url>", re.MULTILINE + re.IGNORECASE)

    def response(self):
        message = "Can't connect to cat API =("
        params = {'format': 'xml', 'type': 'gif'}

        r = requests.get('http://thecatapi.com/api/images/get', params=params)

        if r.status_code == 200:
            response = r.text

            res = re.search(self.RE_URL, response)
            if res:
                message = res.groups()[0]

        return message