

class Data(object):

    def __str__(self):
        return self.__dict__


class ResData(Data):

    def __init__(self, state_code=10000, data=None, msg=None):
        self.state = state_code
        self.data = data
        self.msg = msg

