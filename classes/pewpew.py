import pygame,math
from classes.entity import Entity
from util.grefs import grefs

class Pewpew(Entity):
    def __init__(self):
        self.x = 32
        self.y = 32
        self.width = 16
        self.height = 16

        self.playerX = grefs["Player"].x
        self.playerY = grefs["Player"].y
        grefs["pewpew"] = self
        self.mouse = grefs["MouseMachine"].mouse_stuff

        self.frame = 0
        self.dir = 0
        self.base_image = pygame.transform.scale_by(pygame.image.load("assets\images\entites\pewpew\Luger.png"),0.5)
        
    def updatePosition(self):
        if self.mouse["pos"]:
            # Get player position
            player_x, player_y = grefs["Player"].x+3, grefs["Player"].y+3

            # Get mouse position
            mouse_x, mouse_y = self.mouse["pos"]

            # Calculate angle to mouse
            angle = math.atan2(mouse_y - player_y-8, mouse_x - player_x-8)

            # Set radius of circular motion
            radius = 10  # Adjust as needed

            # Position Pewpew on the circle
            self.x = player_x + math.cos(angle) * radius
            self.y = player_y + math.sin(angle) * radius

            # Convert angle to degrees for rotation
            angle_degrees = math.degrees(angle)

            # Determine if the image should be flipped
            flipped = mouse_x < player_x
            base_image = pygame.transform.flip(self.base_image, flipped, False)

            if flipped:
                angle_degrees += 180

            # Rotate the image to face the mouse
            self.image = pygame.transform.rotate(base_image, -angle_degrees+10)
