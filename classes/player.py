import pygame, math
from classes.entity import Entity
from util.grefs import grefs
from util.image_manager import ImageManager

class Player(Entity):
    def __init__(self):
        self.x = 320 / 2 - 8
        self.y = 180 / 2 - 8
        self.width = 16
        self.height = 16

        self.speed = 1
        self.dash_speed = 3  # Speed multiplier for dashing
        self.dash_cooldown = 2000  # Cooldown in milliseconds
        self.dash_duration = 200  # Dash duration in milliseconds
        self.last_dash_time = -self.dash_cooldown  # Track last dash usage
        self.is_dashing = False
        
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
        current_time = pygame.time.get_ticks()  # Convert to milliseconds
        
        if self.events.get("keyShiftDown", False) and current_time - self.last_dash_time >= self.dash_cooldown:
            self.is_dashing = True
            self.last_dash_time = current_time
            self.dash_end_time = current_time + self.dash_duration
        
        speed_multiplier = self.dash_speed if self.is_dashing else 1
        movement = pygame.math.Vector2(0, 0)
        
        if self.events.get("keyWDown", False):
            movement.y -= 1
        if self.events.get("keySDown", False):
            movement.y += 1
        if self.events.get("keyDDown", False):
            movement.x += 1
        if self.events.get("keyADown", False):
            movement.x -= 1
        
        if movement.length() > 0:
            movement = movement.normalize() * self.speed * speed_multiplier / self.dt
            self.velocity = movement
            if movement.x > 0:
                self.dir = 1
            elif movement.x < 0:
                self.dir = 3
            elif movement.y > 0:
                self.dir = 0
            elif movement.y < 0:
                self.dir = 2
        
        if self.is_dashing and current_time >= self.dash_end_time:
            self.is_dashing = False
        
        if self.velocity.length() > 0:
            move_vector = self.velocity * self.dt

            new_x = self.x + move_vector.x
            new_y = self.y + move_vector.y
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
        self.frame += self.dt * self.speed * (22 if self.is_dashing else 12)  # 12 is FPS
        if self.frame >= 8:  # Reset Frames if more than the 8 frames that we have
            self.frame = 0
        self.image = self.images[self.state, math.floor(self.frame), self.dir]

    def checkCollision(self, rect):
        return pygame.Rect.collidelistall(rect, [
            pygame.Rect(-4, -4, 328, 4),
            pygame.Rect(-4, -4, 4, 188),
            pygame.Rect(-4, 180, 328, 4),
            pygame.Rect(320, -4, 4, 188),
        ])
