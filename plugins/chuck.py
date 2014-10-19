import requests

class ChuckNorrisPlugin():

    help = "Post a random Chuck's phrase"
    command = "chuck"

    @staticmethod
    def response():

        message = "Can't connect to Chuck API =("
        params = {'limitTo': '[nerdy]'}

        r = requests.get('http://api.icndb.com/jokes/random', params=params)

        if r.status_code == 200:
            response = r.json()

            if response['type'] == 'success':
                message = response['value']['joke']

        return message