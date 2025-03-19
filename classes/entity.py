import pygame
from util.grefs import grefs

class Entity:
    def __init__(self,cords:tuple,size:tuple=(16,16),image=None):
        """Spawns an entity that has basic varibles:"""
        self.x = cords[0]
        self.y = cords[1]
        self.width = size[0]
        self.height = size[1]
        self.image = image
    
    def draw(self):
        """Draws the self.image to the window"""
        grefs["main"].window.blit(self.image,(self.x,self.y))
        