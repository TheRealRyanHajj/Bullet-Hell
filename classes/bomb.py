import pygame, math
from classes.entity import Entity
from classes.zombie import Zombie
from util.grefs import grefs

class Bomb(Entity):
    def __init__(self, targetPos):
        self.x = grefs["Player"].x
        self.y = grefs["Player"].y

        self.targetX = targetPos[0] - 8
        self.targetY = targetPos[1] - 8

        self.image = pygame.image.load("assets/images/items.png").subsurface((16*3, 16*13, 16, 16))
        self.explosionImages = [
            pygame.image.load("assets/images/entites/explostionEffect.png").subsurface((32 * i, 32 * 13, 32, 32))
            for i in range(5)
        ]

        self.width = 16  
        self.height = 16  
        self.baseSpeed = 400  # Base speed
        self.exploded = False  
        self.timer = 1.5  
        self.animationTimer = 0  
        self.frame = 0  

        # Arc settings
        self.arcHeight = 30  
        self.progress = 0  
        self.startX, self.startY = self.x, self.y
        self.totalDistance = pygame.math.Vector2(self.targetX - self.x, self.targetY - self.y).length()

        # Direction vector
        direction = pygame.math.Vector2(self.targetX - self.x, self.targetY - self.y)
        if direction.length() > 0:
            self.velocity = direction.normalize()
        else:
            self.velocity = pygame.math.Vector2(0, 0)

    def updatePosition(self):
        if self.exploded:
            self.updateAnimation()
            return  

        dt = grefs["TimeMachine"].dt  

        # **Reversed speed curve for natural movement**
        speedFactor = (1 - self.progress) ** 2  
        currentSpeed = self.baseSpeed * max(0.4, speedFactor)  # Keep a minimum speed

        # Move along the straight-line path
        self.x += self.velocity.x * currentSpeed * dt
        self.progress += (currentSpeed * dt) / self.totalDistance  

        # Apply sine wave arc effect
        arcOffset = math.sin(self.progress * math.pi) * self.arcHeight  
        self.y = (self.startY + (self.targetY - self.startY) * self.progress) - arcOffset

        # Check if it reached the target
        if self.progress >= 1 or self.timer <= 0:
            self.explode()

        self.timer -= dt

    def explode(self):
        if self.exploded:
            return
        self.exploded = True

        # Center the explosion effect properly
        self.x -= 8
        self.y -= 8
        self.image = self.explosionImages[0]
        self.frame = 0  
        self.animationTimer = 0  

        explosion_radius = 48  # Maximum range
        max_damage = 250  # Full damage if directly at center

        for obj in grefs["game"].listOfObjects:
            if isinstance(obj, Zombie):  
                # Calculate distance from bomb's **center**
                distance = pygame.math.Vector2(obj.x + obj.width / 2 - (self.x + self.width / 2), 
                                            obj.y + obj.height / 2 - (self.y + self.height / 2)).length()
                
                if distance < explosion_radius:
                    # Scale damage based on proximity (closer = more damage)
                    damage_factor = 1 - (distance / explosion_radius)  
                    obj.takeDamage(max_damage * damage_factor, self)

                    # Apply knockback (scaled as well)
                    knockback_dir = pygame.math.Vector2(obj.x - self.x, obj.y - self.y)
                    if knockback_dir.length() > 0:
                        obj.velocity += knockback_dir.normalize() * (200 * damage_factor)  
 

    def updateAnimation(self):
        dt = grefs["TimeMachine"].dt  
        self.animationTimer += dt  

        if self.animationTimer > 0.1:  # Change frame every 0.1s
            self.animationTimer = 0  
            self.frame += 1  
            
            if self.frame < len(self.explosionImages):
                self.image = self.explosionImages[self.frame]
            else:
                grefs["game"].listOfObjects.remove(self)  # Remove after animation
