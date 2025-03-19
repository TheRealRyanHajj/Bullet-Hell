import pygame,math
from classes.entity import Entity
from util.grefs import grefs
from util.image_manager import ImageManager

class Player(Entity):
    def __init__(self):
        self.x = 320/2 -8
        self.y = 180/2 -8
        self.width = 16
        self.height = 16

        self.speed = 1
        self.velocity = pygame.math.Vector2(0, 0)
        self.mask = pygame.mask.Mask((16, 10), True)  # Collision mask
        self.maskSurface = self.mask.to_surface()
        self.dt = grefs["TimeMachine"].dt
        self.events = grefs["EventMachine"].key_states
        grefs["Player"] = self


        self.frame = 0
        self.dir = 0
        self.images = ImageManager.createPlayerFrames()   
        
    def updatePosition(self):
        self.velocity = pygame.math.Vector2(0, 0)
        if self.events.get("keyWDown", False):
            self.velocity.y = -self.speed
            self.dir = 2
        if self.events.get("keySDown", False):
            self.velocity.y = self.speed
            self.dir = 0
        if self.events.get("keyDDown", False):
            self.velocity.x = self.speed
            self.dir = 1
        if self.events.get("keyADown", False):
            self.velocity.x = -self.speed
            self.dir = 3
        if self.velocity.length() > 0:  # Normalize movement vector
            move_vector = self.velocity.normalize() * self.speed * self.dt

            new_x = self.x + self.velocity.x
            new_y = self.y + self.velocity.y
            temp_rect = pygame.Rect(new_x, self.y, self.width, self.height)
            if not self.checkCollision(temp_rect):
                self.x = new_x
                self.state = "Run"
            temp_rect = pygame.Rect(self.x, new_y, self.width, self.height)
            if not self.checkCollision(temp_rect):
                self.y = new_y
                self.state = "Run"
        else:
            self.state = "Idle"
            
    def updateAnimation(self):
        self.frame += self.dt * self.speed * 12 # 12 is FPS
        if self.frame >= 8: # Reset Frames if more than the 8 frames that we have
            self.frame = 0
        self.image = self.images[self.state,math.floor(self.frame),self.dir]

    def checkCollision(self,rect):
        return pygame.Rect.collidelistall(rect,[pygame.Rect(-4,-4,328,4),pygame.Rect(-4,-4,4,188),pygame.Rect(-4,180,328,4),pygame.Rect(320,-4,4,188),])
        

        
    

