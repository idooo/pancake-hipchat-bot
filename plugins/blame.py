
class BlamePlugin():

    help = "Blame somebody"
    command = "blame"

    @staticmethod
    def response(random_user):
        message = '{}, this is your fault!'
        return message.format(random_user)