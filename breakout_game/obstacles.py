from turtle import Turtle


class Obstacle:
    def __init__(self):
        self.all_obstacles = []

    def create_obstacle(self, color, x, y):
        new_obstacle = Turtle(shape="square")
        new_obstacle.shapesize(stretch_wid=1, stretch_len=2)
        new_obstacle.color(color)
        new_obstacle.penup()
        new_obstacle.goto(x=x, y=y)
        self.all_obstacles.append(new_obstacle)
