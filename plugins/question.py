import random

class AskMePlugin():

    help = "Ask me a question"
    command = "?"

    @staticmethod
    def response(author):
        options = ['yes', 'no', 'no way!', 'yep!']
        return '{0}, {1}'.format(author, random.choice(options))