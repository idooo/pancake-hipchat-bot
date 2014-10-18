import requests

class GiphyPlugin():

    help = "Get a random gif, with a optional search term (/gif keyboard cat)"
    command = "gif"

    @staticmethod
    def response(message):
        search_values = message.split('/gif', 1)
        tags = ''
        if len(search_values) == 2:
            tags = '+'.join(search_values[1].split())

        r = requests.get('http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag=' + tags)

        if r.status_code == 200:
            response = r.json()
            return response['data']['image_url']

        else:
            return "Can't connect to giphy API =("
