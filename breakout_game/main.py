import time
from turtle import *

from breakout_game.ball import Ball
from breakout_game.obstacles import Obstacle
from breakout_game.paddle import Paddle
from breakout_game.scoreboard import Scoreboard

# Create screen
screen = Screen()
screen.bgcolor("black")
screen.setup(width=900, height=900)
screen.title("Breakout")
screen.tracer(0)

# Create paddle
paddle = Paddle(0, -350)

# Create ball
ball = Ball()

# Hit counter
counter = 0

# Current window
num_window = 1

# Amount attempts left
attempts = 3

# Check if the paddle hit the ball for the 4th time
hit_4 = False
# Check if the paddle hit the ball for the 12th time
hit_12 = False
# Check if the paddle hit the first orange line
hit_first_orange = False
# Check if the paddle hit the second orange line
hit_second_orange = False
# Check if the paddle hit the first red line
hit_first_red = False
# Check if the paddle hit the second red line
hit_second_red = False
# Check if the game is still running
game_is_on = True

# Get user input
screen.listen()
screen.onkeypress(key="d", fun=paddle.move_right)
screen.onkeypress(key="a", fun=paddle.move_left)

# Create obstacle generator
obs = Obstacle()
# Create scoreboard
scoreboard = Scoreboard()
scoreboard.show_score()

# Score of each block color
score_table = {"yellow": 1, "green": 3, "orange": 5, "red": 7, }


def create_blocks():
    """
    Generate obstacles blocks
    """
    for i in range(-420, 440, 65):
        obs.create_obstacle(color="red", x=i, y=380)
    for i in range(-420, 440, 65):
        obs.create_obstacle(color="red", x=i, y=350)
    for i in range(-420, 440, 65):
        obs.create_obstacle(color="orange", x=i, y=320)
    for i in range(-420, 440, 65):
        obs.create_obstacle(color="orange", x=i, y=290)
    for i in range(-420, 440, 65):
        obs.create_obstacle(color="green", x=i, y=260)
    for i in range(-420, 440, 65):
        obs.create_obstacle(color="green", x=i, y=230)
    for i in range(-420, 440, 65):
        obs.create_obstacle(color="yellow", x=i, y=200)
    for i in range(-420, 440, 65):
        obs.create_obstacle(color="yellow", x=i, y=170)


create_blocks()

while game_is_on:
    # Move the ball
    time.sleep(1 / ball.move_speed)
    ball.move()

    # Detect obstacle collision
    for obstacle in obs.all_obstacles:
        if ball.distance(obstacle) < 40:
            scoreboard.score += score_table[obstacle.color()[0]]
            obstacle.hideturtle()
            obs.all_obstacles.remove(obstacle)
            ball.bounce("y")

    # Detect wall collision
    if ball.xcor() > 430 or ball.xcor() < -430:
        ball.bounce("x")
    elif ball.ycor() > 380:
        paddle.shapesize(stretch_len=3)
        ball.bounce("y")

    # Increment speed
    if counter == 4 and not hit_4:
        ball.move_speed = 20
        hit_4 = True
    if counter == 12 and not hit_12:
        ball.move_speed = 40
        hit_12 = True
    if ball.ycor() > 290 and not hit_first_orange:
        ball.move_speed = 50
    if ball.ycor() > 320 and not hit_second_orange:
        ball.move_speed = 60
        hit_second_orange = True
    if ball.ycor() > 350 and not hit_first_red:
        ball.move_speed = 70
    if ball.ycor() > 380 and not hit_second_red:
        ball.move_speed = 80
        hit_second_red = True

    # Detect paddle collision
    if ball.distance(paddle) < 75 and ball.ycor() < -330:
        counter += 1
        ball.bounce("y")

    # Detect if the ball hit the bottom of the screen
    if ball.ycor() < -440:
        attempts -= 1
        ball.home()
        ball.bounce("y")
    # Check if the player ran out of attempts
    if attempts == 0:
        game_is_on = False
    # Generate a new set of blocks when the first window is completed
    if not obs.all_obstacles:
        if num_window == 1:
            create_blocks()
            paddle.shapesize(stretch_len=6)
            ball.home()
            ball.move_speed = 10
            counter = 0
            num_window += 1
        else:
            game_is_on = False
    scoreboard.show_score()
    screen.update()
# Close screen
scoreboard.game_over()
screen.exitonclick()
