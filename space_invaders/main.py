from random import choice
from turtle import *

from space_invaders.alien_laser import AlienLaser
from space_invaders.alien_manager import AlienManager
from space_invaders.obstacle_manager import ObstacleGenerator
from space_invaders.player import Player
from space_invaders.player_laser import PlayerLaser
from space_invaders.scoreboard import Scoreboard

# Config the screen
screen = Screen()
screen.tracer(0)
screen.setup(height=800, width=700)
screen.bgcolor("black")
# Register the shapes used in this project
screen.register_shape("./assets/player_ship.gif")
screen.register_shape("./assets/an_alien.gif")
screen.register_shape("./assets/silly_alien.gif")
screen.register_shape("./assets/space_squid.gif")
# Create player instance
player = Player()
# Create scoreboard
scoreboard = Scoreboard()
# Initialize alien manager
alien_manager = AlienManager()
# Generate aliens
alien_manager.generate_aliens()
# Initialize obstacle manager
obstacle_generator = ObstacleGenerator()
# Generate obstacle
obstacle_generator.generate()
# Generate first frame
screen.update()
# Listen to player's input
screen.listen()
screen.onkeypress(key="a", fun=player.move_left)
screen.onkeypress(key="d", fun=player.move_right)
screen.onkey(key="space", fun=lambda: laser.shoot(player.xcor()))

# Initialize the player's laser
laser = PlayerLaser(player.xcor())

# Set initial values
hit_limit = False
direction = 1
laser_state = False
enemies_lasers = []
game_is_on = True
# Generate life counter
lives = []
for l in range(2):
    life = Turtle()
    life.shape("./assets/player_ship.gif")
    life.penup()
    life.goto(-300 + 50 * l, -370)
    lives.append(life)

# Main loop
while game_is_on:
    # Check if the laser hit upper wall
    if laser.get_y() > 400:
        laser.destroy_instance()
    else:
        if laser.state:
            laser.move()
    # Redirect the movement when the aliens hit a wall
    if alien_manager.check_limits():
        direction *= -1
    # Move aliens
    if direction == 1:
        alien_manager.move_all_right()
    else:
        alien_manager.move_all_left()
    # Loop through aliens list
    for alien in alien_manager.all_aliens:
        # Check for collisions
        if alien.distance(laser) < 20:
            alien_manager.aliens_left -= 1
            scoreboard.score += alien.value
            alien.hideturtle()
            laser.destroy_instance()
            alien_manager.all_aliens.remove(alien)
        # Randomly generate alien lasers
        dice = choice(range(1, 1000))
        if dice == 1:
            new_laser = AlienLaser(alien.xcor(), alien.ycor())
            enemies_lasers.append(new_laser)
    # Loop through enemies laser list
    for enemy_laser in enemies_lasers:
        # Check for collisions with the player
        if enemy_laser.distance(player) < 20:
            player.goto(0, -300)
            lives[-1].hideturtle()
            lives.pop()
        # Check for collisions with players laser
        if enemy_laser.distance(laser) < 5:
            laser.destroy_instance()
            enemy_laser.hideturtle()
            enemies_lasers.remove(enemy_laser)
        enemy_laser.move()
    # Loop through obstacle list
    for obstacle in obstacle_generator.all_obstacles:
        # Check for collision with alien lasers
        for enemy_laser in enemies_lasers:
            if obstacle.distance(enemy_laser) < 5:
                obstacle.hideturtle()
                obstacle_generator.all_obstacles.remove(obstacle)
                enemy_laser.hideturtle()
                enemies_lasers.remove(enemy_laser)
        # Check for collision with the player's laser
        if obstacle.distance(laser) < 8:
            obstacle.hideturtle()
            obstacle_generator.all_obstacles.remove(obstacle)
            laser.destroy_instance()
        # End the game when all aliens are destroyed
        if alien_manager.aliens_left < 1:
            game_is_on = False
        # End game when the player runs out of lives
        if not lives:
            game_is_on = False
    # Update scoreboard
    scoreboard.show_score()
    # Update window
    screen.update()

# Set up the game over screen
screen.clear()
screen.bgcolor("black")
scoreboard.game_over()
# Exit screen
screen.exitonclick()
