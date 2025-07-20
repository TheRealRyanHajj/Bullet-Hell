import pygame
from states.states import State
from util.grefs import grefs
from classes.entity import Entity
from classes.player import Player
from classes.pewpew import Pewpew
from classes.bullet import Bullet
from classes.bomb import Bomb
from classes.zombie import Zombie
from util.bullet_manager import BulletManager
from util.bomb_manager import BombManager
from util.zombie_manager import ZombieManager

class GameState(State):
    def __init__(self, state_machine):
        self.state_machine = state_machine
        
    def enter(self):
        grefs["game"] = self
        self.Player = Player()
        self.Pewpew = Pewpew()
        self.listOfObjects = [self.Pewpew, self.Player]
        self.listOfBullets = []
        self.mouse = grefs["MouseMachine"].mouse_stuff
        self.ZombieManager = ZombieManager()
        self.BulletManager = BulletManager()
        self.BombManager = BombManager()
        self.bulletDamage = 50
        self.bg = pygame.image.load("assets/images/bg.png")

    def update(self,window):
        self.window = window
        self.ZombieManager.update()
        self.Player.updatePosition()
        self.Pewpew.updatePosition()
        
        self.BulletManager.updateCooldown()
        self.BombManager.updateCooldown()

        if self.mouse["left"]:
            if self.BulletManager.canSpawnNewBullet():
                self.listOfObjects.append(Bullet())
        if self.mouse["right"]:
            if self.BombManager.canSpawnNewBomb():
                self.listOfObjects.append(Bomb(self.mouse["pos"]))

        for each in self.listOfObjects:
            if isinstance(each, (Bullet, Zombie, Bomb)):
                each.updatePosition()

        for bullet in self.listOfObjects:
            if isinstance(bullet, Bullet):
                for zombie in self.listOfObjects:
                    if isinstance(zombie, Zombie):
                        if bullet.rect.colliderect(zombie.bulletRect) and zombie.canTakeDamage:
                            zombie.takeDamage(self.bulletDamage,self.Player)
                            self.listOfObjects.remove(bullet)
                            break

        self.Player.updateAnimation()
        for each in self.listOfObjects:
            if isinstance(each, (Zombie)):
                each.updateAnimation()

        self.window.blit(self.bg, (0, 0))

        self.listOfObjects.sort(key=lambda obj: obj.y + obj.height)

        for each in self.listOfObjects:
            each.draw()

        for each in self.listOfObjects:
            if isinstance(each, Zombie):
                each.drawHealthBar()
        self.Player.drawUi()
        self.ZombieManager.drawUi()

    def exit(self):
        ...
