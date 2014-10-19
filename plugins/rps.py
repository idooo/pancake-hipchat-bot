import random

class RPSPlugin():

    help = "Rock - Paper - Scissors - Lizard - Spock (type '/rps help' for help)"
    command = "rps"

    @staticmethod
    def response(message, author):
        if 'help' in message:
            return 'http://a.tgcdn.net/images/products/additional/large/db2e_lizard_spock.jpg'

        options = ['Rock', 'Paper', 'Scissors', 'Lizard', 'Spock']
        return '{0} - {1}'.format(author, random.choice(options))