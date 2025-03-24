import pygame, math
from classes.entity import Entity
from util.grefs import grefs
from util.image_manager import ImageManager

class Zombie(Entity):
    def __init__(self, x, y, health):
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16

        self.speed = 50  # Slower than player
        self.velocity = pygame.math.Vector2(0, 0)
        self.mask = pygame.mask.Mask((16, 10), True)  # Collision mask
        self.maskSurface = self.mask.to_surface()
        self.dt = grefs["TimeMachine"].dt
        self.target = grefs.get("Player", None)  # Track the player
        
        self.health = health  # Health stat
        self.max_health = health 
        self.canTakeDamage = True
        
        self.frame = 0
        self.dir = 0
        self.state = "Run"
        self.images = ImageManager.createZombieFrames()  # Use zombie-specific frames

        self.screen = grefs["main"].window

        # Create a rect for collision detection
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def updatePosition(self):
        if not self.target or self.health <= 0:
            return
        
        direction = pygame.math.Vector2(self.target.x - self.x, self.target.y - self.y)
        if direction.length() > 5:
            direction = direction.normalize()
            self.velocity = direction * self.speed * self.dt
            self.x += self.velocity.x
            self.y += self.velocity.y
            self.state = "Run"

            # Determine movement direction
            if abs(direction.x) > abs(direction.y)/4:  # Moving more in X direction
                self.dir = 1 if direction.x > 0 else 3  # Right or Left
            else:  # Moving more in Y direction
                self.dir = 2 if direction.y < 0 else 0  # Up or Down
        else:
            self.state = "Idle"

        # Update the rect position based on the zombie's new position
        self.rect.topleft = (self.x, self.y)

    def takeDamage(self, amount):
        if not self.canTakeDamage:
            return
        self.health -= amount
        if self.health <= 0:
            self.y -= 16
            self.state = "Death"  # Change state to "Death" when health is 0 or less
            self.frame = 0
            self.canTakeDamage = False
            grefs["ZombieManager"].zombiesKilled += 1
        else:
            self.state = "Hurt"  # Change state to "Hurt" when taking damage
            self.frame = 0  # Reset frame to ensure the hurt animation displays properly

    def updateAnimation(self):
        if self.state == "Hurt":
            self.image = self.images.get(("Hurt", 0, self.dir))  # Single frame for Hurt state
        elif self.state == "Death":
            self.frame += self.dt * self.speed/4  # 12 FPS for death animation
            if self.frame >= 8:  # After 8 frames, remove the zombie
                self.frame = 0
                # Remove zombie from listOfObjects (ensure it's removed in the main game loop)
                if self in grefs["game"].listOfObjects:
                    grefs["game"].listOfObjects.remove(self)
            self.image = self.images.get(("Death", math.floor(self.frame), self.dir), self.images.get(("Idle", 0, self.dir)))
        else:
            self.frame += self.dt * self.speed/4  # 12 FPS
            if self.frame >= 8:
                self.frame = 0
            self.image = self.images.get((self.state, math.floor(self.frame), self.dir), self.images.get(("Idle", 0, self.dir)))

    def drawHealthBar(self):
        if self.health > 0:
            bar_width = 20
            bar_height = 3
            fill = (self.health / self.max_health) * bar_width
            outline_rect = pygame.Rect(self.x - 2, self.y - 6, bar_width, bar_height)
            fill_rect = pygame.Rect(self.x - 2, self.y - 6, fill, bar_height)
            pygame.draw.rect(self.screen, (255, 0, 0), outline_rect)  # Red background
            pygame.draw.rect(self.screen, (0, 255, 0), fill_rect)  # Green health
