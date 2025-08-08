from turtle import Turtle


class PlayerLaser(Turtle):
    def __init__(self, xpos):
        super().__init__()
        # Config laser format
        self.penup()
        self.tiltangle(90)
        self.setpos(xpos, -275)
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=0.3, stretch_len=1)
        self.hideturtle()
        # Check if the is already an laser on the screen
        self.state = False

    def move(self):
        """
        Move the laser upwards
        """
        self.sety(self.ycor() + 6)

    def get_y(self) -> int:
        """
        :return: y position of the laser
        """
        return self.ycor()

    def destroy_instance(self):
        """
        Resets laser to the original state
        """
        self.state = False
        self.hideturtle()
        self.sety(-275)

    def shoot(self, xpos: int):
        """
        Triggers the laser
        :param xpos: x position of the player
        """
        if not self.state:
            self.state = True
            self.setx(xpos)
            self.showturtle()
