import random
import pygame
from classes.zombie import Zombie
from util.grefs import grefs

class ZombieManager:
    def __init__(self):
        self.wave = 0
        self.spawn_timer = 0
        self.spawn_interval = 2000  # Base interval
        self.zombies_remaining = 0
        self.total_zombies = 0
        self.current_time = pygame.time.get_ticks()
        self.window = grefs["main"].window
        grefs["ZombieManager"] = self
        self.difficulty = 2
        self.spawn_positions = [
            (-64, i) for i in range(0, 200, 20)
        ] + [
            (384, i) for i in range(0, 200, 20)
        ] + [
            (i, -64) for i in range(0, 380, 20)
        ] + [
            (i, 244) for i in range(0, 380, 20)
        ]
    
    def spawn_next_wave(self):
        self.wave += 1
        self.zombiesKilled = 0
        self.total_zombies = round(self.wave * self.difficulty)
        self.zombies_remaining = self.total_zombies  # Set total for tracking
        self.spawn_timer = self.current_time

        if self.wave == 25:
            pass  # Spawn boss logic here

    def update(self):
        self.current_time = pygame.time.get_ticks()
        self.checkWaveCompleted()

        if self.zombies_remaining > 0 and self.current_time - self.spawn_timer >= self.spawn_interval:
            spawn_count = min(self.zombies_remaining, random.randint(2, 5))
            for _ in range(spawn_count):
                self.spawn_zombie()
                self.zombies_remaining -= 1

            self.spawn_timer = self.current_time
            self.spawn_interval = random.randint(300, 700)  # Vary spawn interval

    def spawn_zombie(self):
        x, y = random.choice(self.spawn_positions)
        new_zombie = Zombie(x, y, (((self.wave-1)/10)+1)*100)
        grefs["game"].listOfObjects.append(new_zombie)

    def checkWaveCompleted(self):
        if all(not isinstance(obj, Zombie) for obj in grefs["game"].listOfObjects) and self.zombies_remaining == 0:
            self.spawn_next_wave()

    def get_wave_completion_percentage(self):
        if self.total_zombies == 0:
            return 100
        return int((self.zombiesKilled / self.total_zombies) * 100)

    def drawUi(self):
        percentage = self.get_wave_completion_percentage()
        bar_width = 200
        bar_height = 4
        bar_x = (320 - bar_width) // 2
        bar_y = 4
        fill_width = (percentage / 100) * bar_width
        
        pygame.draw.rect(self.window, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))  # Background bar
        pygame.draw.rect(self.window, (0, 255, 0), (bar_x, bar_y, fill_width, bar_height))  # Green fill