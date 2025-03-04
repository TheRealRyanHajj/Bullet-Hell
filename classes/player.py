import pygame
from entity import Entity
from util.grefs import grefs
from util.image_manager import ImageManager

class Player(Entity):
    def __init__(self):
        self.speed = 50
        self.velocity = pygame.math.Vector2(0, 0)
        self.mask = pygame.mask.Mask((16, 10), True)  # Collision mask
        self.maskSurface = self.mask.to_surface(dest=(8, 24))  # Convert mask to surface
        self.dt = grefs["TimeMachine"].dt
        self.events = grefs["EventMachine"].key_states
        self.frame = 0

        self.images = ImageManager.createFrames()   
        
    def updatePosition(self):
        if self.events.get("keyWDown", False):
            self.velocity.y = -self.speed
        if self.events.get("keyADown", False):
            self.velocity.x = -self.speed
        if self.events.get("keySDown", False):
            self.velocity.y = self.speed
        if self.events.get("keyDDown", False):
            self.velocity.x = self.speed
        if vector.length() > 0:  # Normalize movement vector
            if vector.x != 0 and vector.y != 0:
                vector = vector * self.speed*1 * self.dt
            else:
                vector = vector * self.speed * self.dt
            new_x = self.x + vector.x
            new_y = self.y + vector.y
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
        self.frame += self.dt * 12 # 12 is FPS
        if self.frame >= 4: # Reset Frames if more than the 4 frames that we have
            self.frame = 0
        if self.state == "Run":
            image = 

    def checkCollision(self,rect):
        return pygame.Rect.collidelistall(rect,[pygame.Rect(-4,-4,328,4),pygame.Rect(-4,-4,4,188),pygame.Rect(-4,180,328,4),pygame.Rect(320,-4,4,188),])
        

        
    

