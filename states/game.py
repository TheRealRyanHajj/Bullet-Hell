import pygame
from states.states import State
from util.grefs import grefs
from classes.entity import Entity
from classes.player import Player

class GameState(State):
    def __init__(self, state_machine):
        self.state_machine = state_machine
        
    def enter(self):
        self.window = grefs["main"].window
        self.Player = Player()


    def update(self):
        events = grefs["EventMachine"].key_states
        self.window.fill((255,255,255))
        self.Player.updatePosition()
        self.Player.updateAnimation()
        self.Player.draw()

    def exit(self):
        ...