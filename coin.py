
class Coin(object):
    """ super class for all coin objects ... """

    def __init__(self):
        self.area = 0
        self.volume = 0

    def calculate_shape(self):
        pass

    def generate_shape(self, volume):
        pass

    def draw(self, canvas):
        pass

    def image(self):
        """ should return a PIL Image """
        raise NotImplementedError("Should return PIL image")

    def __str__(self):
        return "Coin"