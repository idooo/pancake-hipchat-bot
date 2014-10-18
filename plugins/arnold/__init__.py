import random

from arnold_phrases import ARNOLD_PHRASES

class ArnoldPlugin():

    help = "Arnold Schwarzenegger's phrase (/! name)"
    command = "!"

    @staticmethod
    def response(mentioned_user, random_user):

        phrase = random.choice(ARNOLD_PHRASES)

        if "{}" not in phrase:
            phrase = "{}, " + phrase

        username = mentioned_user

        if not username:
            username = random_user

        return phrase.format(username)