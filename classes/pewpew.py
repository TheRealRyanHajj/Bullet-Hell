import pygame,math
from classes.entity import Entity
from util.grefs import grefs
from util.image_manager import ImageManager

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
        self.base_image = pygame.image.load("") 
        
    def updatePosition(self):
        if self.mouse["pos"]:
            ...
        
    

