from turtle import Turtle


class Player(Turtle):
    def __init__(self):
        super().__init__()
        # Config the player shape
        self.laser_on_screen = False
        self.penup()
        self.setpos(0, -300)
        self.shape("./assets/player_ship.gif")

    def move_left(self):
        """
        Moves the player to the left when the player presses 'a'
        """
        if self.xcor() > -330:
            self.goto(self.xcor() - 10, self.ycor())

    def move_right(self):
        """
        Moves the player to the right when the player presses 'd'
        """
        if self.xcor() < 330:
            self.goto(self.xcor() + 10, self.ycor())
