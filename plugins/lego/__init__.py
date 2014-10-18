import random

from lego_quotes import LEGO_QUOTES

class LegoPlugin():

    help = "LEGO Movie quote's (/lego name)"
    command = "lego"

    @staticmethod
    def response(mentioned_user, random_user):

        phrase = random.choice(LEGO_QUOTES)

        if "{}" not in phrase:
            phrase = "{}, " + phrase

        username = mentioned_user

        if not username:
            username = random_user

        return phrase.format(username)