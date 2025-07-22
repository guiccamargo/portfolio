from turtle import Turtle

SHAPE = "square"
COLOR = "blue"


class Paddle(Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.shape(SHAPE)
        self.color(COLOR)
        self.penup()
        self.shapesize(stretch_wid=0.7, stretch_len=6)
        self.goto(x=x, y=y)

    def move_left(self):
        if self.xcor() > -380:
            self.goto(x=self.xcor() - 20, y=self.ycor())

    def move_right(self):
        if self.xcor() < 380:
            self.goto(x=self.xcor() + 20, y=self.ycor())
