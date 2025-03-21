import pygame,math
from classes.entity import Entity
from util.grefs import grefs

class Bullet(Entity):
    def __init__(self):
        self.x = grefs["pewpew"].x
        self.y = grefs["pewpew"].y
        self.width = 8
        self.height = 8

        self.mouse = grefs["MouseMachine"].mouse_stuff
        self.speed = 10  # Adjust speed as needed

        # Calculate direction vector
        mouse_x, mouse_y = self.mouse["pos"]
        angle = math.atan2(mouse_y - self.y, mouse_x - self.x)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed
        self.image = pygame.transform.scale_by(pygame.image.load("assets/images/entites/bullets/black.png"),0.5)

    def updatePosition(self):
        # Move the bullet in the calculated direction
        self.x += self.dx
        self.y += self.dy
