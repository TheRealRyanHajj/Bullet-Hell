import pygame
from states.states import State
from util.grefs import grefs
from classes.entity import Entity
from classes.player import Player
from classes.pewpew import Pewpew
from classes.bullet import Bullet
from classes.zombie import Zombie
from util.bullet_manager import BulletManager

class GameState(State):
    def __init__(self, state_machine):
        self.state_machine = state_machine
        
    def enter(self):
        self.window = grefs["main"].window
        self.Player = Player()
        self.Pewpew = Pewpew()
        self.listOfObjects = [self.Pewpew,self.Player,Zombie(16,16)]
        self.listOfBullets = []
        self.mouse = grefs["MouseMachine"].mouse_stuff
        self.BulletManager = BulletManager()

    def update(self):
        self.window.fill((255,255,255))
        self.Player.updatePosition()
        self.Pewpew.updatePosition()
        self.BulletManager.updateCooldown()
        if self.mouse["left"]: #if mouse left pressed
            if self.BulletManager.canSpawnNewBullet():
                self.listOfObjects.append(Bullet())

        for each in self.listOfObjects:
            if isinstance(each,(Bullet,Zombie)):
                each.updatePosition()

        self.Player.updateAnimation()

        self.listOfObjects.sort(key=lambda obj: obj.y+obj.height)
        for each in self.listOfObjects:
            each.draw()

        for each in self.listOfObjects:
            if isinstance(each,(Zombie)):
                each.drawHealthBar()

    def exit(self):
        ...