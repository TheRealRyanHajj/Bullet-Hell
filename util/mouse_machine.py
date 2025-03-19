import pygame
pygame.init()
from util.grefs import grefs

class MouseMachine:
    def __init__(self):
        grefs["MouseMachine"] = self
        self.mouse_stuff = {}

    def update(self):
        self.mouse_stuff["pos"] = pygame.mouse.get_pos()
        self.mouse_stuff["left"] = pygame.mouse.get_pressed()[0]
        self.mouse_stuff["right"] = pygame.mouse.get_pressed()[2]
