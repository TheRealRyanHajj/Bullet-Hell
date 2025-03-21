import pygame, math
from classes.entity import Entity
from util.grefs import grefs

class Bullet(Entity):
    def __init__(self):
        self.x = grefs["pewpew"].x
        self.y = grefs["pewpew"].y
        self.width = 4
        self.height = 4

        self.mouse = grefs["MouseMachine"].mouse_stuff
        self.speed = 10  # Adjust speed as needed

        # Calculate direction vector
        mouse_x, mouse_y = self.mouse["pos"]
        angle = math.atan2(mouse_y - self.y, mouse_x - self.x)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed
        self.image = pygame.transform.scale_by(pygame.image.load("assets/images/entites/bullets/white.png"), 0.4)

        # Create a rect for collision detection
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def updatePosition(self):
        # Move the bullet in the calculated direction
        self.x += self.dx
        self.y += self.dy

        # Update the rect position based on the bullet's new position
        self.rect.topleft = (self.x, self.y)

        # Check if the bullet is off-screen
        if not self.rect.colliderect(pygame.Rect(0, 0, 320, 180)):
            grefs["game"].listOfObjects.remove(self)

    def removeBullet(self):
        # Assuming listOfObjects is where the bullets are stored
        if self in grefs["main"].listOfObjects:
            grefs["main"].listOfObjects.remove(self)
