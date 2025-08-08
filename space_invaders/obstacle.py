from turtle import Turtle


class Obstacle(Turtle):
    def __init__(self, xpos, ypos):
        """
        Config the Obstacle shape
        :param xpos: x position where the obstacle will be placed
        :param ypos: y position where the obstacle will be placed.
        """
        super().__init__()
        self.penup()
        self.tiltangle(90)
        self.setpos(xpos, ypos)
        self.shape("square")
        self.color("green")
        self.shapesize(stretch_wid=0.2, stretch_len=1)
