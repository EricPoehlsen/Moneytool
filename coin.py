from PIL import Image, ImageTk


class Coin(object):
    """ super class for all coin objects ... """

    DIMS = ()
    UNITS = ()
    NAME = "generic"

    def __init__(self):
        self.area = 0
        self.volume = 0

    def calculate_shape(self):
        pass

    def generate_shape(self, volume):
        pass

    def draw(self, canvas):
        """ clear canvas """
        canvas.delete("all")
        image = ImageTk.PhotoImage(self.image)
        canvas.create_image(image)

    def image(self):
        """ should return a PIL Image """
        return Image.new("RGBA", (1,1))

    def __str__(self):
        return "EMPTY"