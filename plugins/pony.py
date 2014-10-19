import random

class PonyPlugin():

    help = "Post a random pony image"
    command = "pony"

    @staticmethod
    def response():
        max_number = 160
        return "http://ponyfac.es/{}/full.jpg".format(random.randint(1, max_number))