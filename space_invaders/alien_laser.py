from turtle import Turtle


class AlienLaser(Turtle):
    def __init__(self, xpos, ypos):
        """
        :param xpos: x position of the alien
        :param ypos: y position of the alien
        """
        super().__init__()
        # Config the laser shape
        self.penup()
        self.tiltangle(90)
        self.setpos(xpos, ypos)
        self.shape("square")
        self.color("green")
        self.shapesize(stretch_wid=0.2, stretch_len=1)

    def move(self):
        """
        Move the laser downwards
        """
        self.sety(self.ycor() - 6)
