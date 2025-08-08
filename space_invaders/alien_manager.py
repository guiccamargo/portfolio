from space_invaders.alien import Alien


class AlienManager:
    """
    This class is used to manage the movement of the aliens.
    """

    def __init__(self):
        self.alien_pace = 1
        self.all_aliens = []
        self.aliens_left = 50

    def generate_aliens(self):
        """
        Set the initial position of the aliens.
        """
        for i in range(-250, 250, 50):
            self.all_aliens.append(Alien("./assets/an_alien.gif", i, 100, 10))
            self.all_aliens.append(Alien("./assets/an_alien.gif", i, 150, 10))
            self.all_aliens.append(Alien("./assets/silly_alien.gif", i, 200, 20))
            self.all_aliens.append(Alien("./assets/silly_alien.gif", i, 250, 20))
            self.all_aliens.append(Alien("./assets/space_squid.gif", i, 300, 30))

    def check_limits(self) -> bool:
        """
        Detect when an alien hit the wall
        :return: True if an alien hit the wall.
        """
        return any(alien.xcor() > 320 for alien in self.all_aliens) or any(
            alien.xcor() < -320 for alien in self.all_aliens)

    def move_all_right(self):
        """
        Move all alien to the right if none of the has hit the wall.
        """
        hit_right_wall = any(alien.xcor() > 320 for alien in self.all_aliens)
        for alien in self.all_aliens:
            if hit_right_wall:
                break
            alien.setx(alien.xcor() + self.alien_pace)

    def move_all_left(self):
        """
        Move all alien to the left if none of the has hit the wall.
        """
        hit_left_wall = any(alien.xcor() < -320 for alien in self.all_aliens)
        for alien in self.all_aliens:
            if hit_left_wall:
                break
            alien.setx(alien.xcor() - self.alien_pace)
