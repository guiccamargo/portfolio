from space_invaders.obstacle import Obstacle


class ObstacleGenerator:
    """
    This class is used to generate the obstacles on screen.
    """

    def __init__(self):
        self.all_obstacles = []

    def generate(self):
        """
        Set the position of the obstacles.
        """
        for i in range(-40, 40, 5):
            for j in range(-i, i, 10):
                self.all_obstacles.append(Obstacle(j - 240, i))
                self.all_obstacles.append(Obstacle(j - 160, i))
                self.all_obstacles.append(Obstacle(j - 80, i))
                self.all_obstacles.append(Obstacle(j, i))
                self.all_obstacles.append(Obstacle(j + 80, i))
                self.all_obstacles.append(Obstacle(j + 160, i))
                self.all_obstacles.append(Obstacle(j + 240, i))
