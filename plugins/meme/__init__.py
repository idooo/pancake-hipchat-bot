import re
import requests

from memes import MEMES

class MemePlugin():

    command = "meme"
    help = "Creates a meme. Type `/" + command + "` to get help"

    matchers = []
    meme_help = ["Creates a meme with one of the following patterns:"]

    def __init__(self):
        for meme in MEMES:
            self.matchers.append({
                'picture': meme['picture'],
                'groups': meme['groups'],
                'pattern': re.compile(meme['pattern'], re.IGNORECASE)
            })
            self.meme_help.append("/" + self.command + " " + meme['help'])

    def __check_matches(self, message):
        message = message.replace('/' + self.command, '').strip()

        for match in self.matchers:
            res = re.search(match['pattern'], message)
            if res:
                obj = {
                    'u': match['picture'],
                    't1': '',
                    't2': ''
                }
                groups = res.groups()

                if (isinstance(match['groups'][0], int) and len(groups) > 0 or
                    match['groups'][0] == '' and isinstance(match['groups'][1], int) and len(groups) > 0):
                    obj['t1'] = groups[0]

                if isinstance(match['groups'][1], int) and len(groups) > 1:
                    obj['t2'] = groups[1]

                return obj

        return None

    def response(self, message):
        default_response = "Do not know about this meme. Try `/" + self.command + "` to get help"

        if message.strip() == '/' + self.command:
            return "\n".join(self.meme_help)

        params = self.__check_matches(message)

        if params:
            r = requests.get('http://memecaptain.com/g', params=params)

            if r.status_code == 200:
                return r.json()['imageUrl']

            return "We have return code " + str(r.status_code) + " here. Very strange..."

        return default_response