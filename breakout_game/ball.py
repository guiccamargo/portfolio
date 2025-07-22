from turtle import Turtle

INITIAL_SPEED = 10


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.penup()
        self.x_move = 10
        self.y_move = 10
        self.move_speed = INITIAL_SPEED

    def move(self):
        """
        Animate the ball
        """
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move

        self.goto(new_x, new_y)

    def bounce(self, axis):
        """
        Chance direction of the ball
        """
        if axis == "x":
            # self.move_speed *= 0.9
            self.x_move *= -1
        elif axis == "y":
            self.y_move *= -1
