
class Coin(object):
    """ super class for all coin objects ... """

    def __init__(self):
        self.area = 0
        self.volume = 0

    def calculate_shape(self):
        pass

    def draw(self, canvas):
        pass

    def __str__(self):
        return "Coin"