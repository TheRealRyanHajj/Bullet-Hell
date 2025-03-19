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
        self.mouse = grefs["MouseMachine"].mouse_stuff

        self.frame = 0
        self.dir = 0
        self.base_image = pygame.image.load("assets\images\entites\pewpew\M92.png") 
        
    def updatePosition(self):
        if self.mouse["pos"]:
            # Move Pewpew to player's position
            self.x, self.y = grefs["Player"].x, grefs["Player"].y

            # Calculate angle to mouse
            mouse_x, mouse_y = self.mouse["pos"]
            angle = math.degrees(math.atan2(mouse_y - self.y, mouse_x - self.x))

            # Rotate the image to face the mouse
            self.image = pygame.transform.rotate(self.base_image, -angle)

        
    

