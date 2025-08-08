from turtle import Turtle


class Alien(Turtle):
    def __init__(self, alien_shape: str, x: int, y: int, value: int):
        """
        Config the Alien shape
        :param alien_shape: link for the alien shape
        :param x: x positon of the alien
        :param y: y position of the alien
        :param value: score to be added when the alien is hit.
        """
        super().__init__()
        self.value = value
        self.penup()
        self.setpos(x, y)
        self.shape(alien_shape)
