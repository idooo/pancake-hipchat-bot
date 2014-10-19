import random

class RollPlugin():

    help = "Roll a random number 0 - 100"
    command = "roll"

    @staticmethod
    def response(author):
        return '{0} rolled {1}'.format(author, random.randint(0, 100))