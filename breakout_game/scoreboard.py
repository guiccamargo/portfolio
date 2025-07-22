from turtle import Turtle

FONT = ("Courier", 32, "bold")


class Scoreboard(Turtle):
    def __init__(self):
        """Initialize ScoreBoard"""
        super().__init__()
        self.score = 0
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(x=-400, y=400)
        self.show_score()

    def show_score(self):
        """Write current score on screen."""
        self.clear()
        self.write(f"{self.score:03d}", align="center", font=FONT)

    def game_over(self):
        """Start Game Over screen."""
        self.home()
        self.color("red")
        self.write(f"Final Score: {self.score:03d}", align="center", font=FONT)
