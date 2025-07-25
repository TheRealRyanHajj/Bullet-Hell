import pygame,sys
from states.states import State
from util.grefs import grefs

class CreditsState(State):
    def __init__(self, state_machine):
        self.state_machine = state_machine

    def enter(self):
        self.dt = grefs["TimeMachine"].dt
        # Load fonts with different sizes
        self.font_small = pygame.font.Font('assets\images\gui\Pixel_NES.otf', 8)
        self.font_medium = pygame.font.Font('assets\images\gui\Pixel_NES.otf', 12)
        self.font_large = pygame.font.Font('assets\images\gui\Pixel_NES.otf', 16)

        # Credit text with associated font size
        self.CREDITS = [
            ("Thank you for playing!", self.font_large),
            ("", self.font_small),
            ("ART", self.font_medium),
            ("Guns: https://greenpixels.itch.io/pixel-art-assets-7", self.font_small),
            ("", self.font_small)
        ]
        # Render text surfaces
        self.text = [font.render(line, True, (255,255,255)) for line, font in self.CREDITS]

        self.offsetY = -202

        
    def update(self,window):
        self.window = window
        self.window.fill((0, 0, 0))
        speed = 1 / float(self.dt)  # Calculate speed factor
        self.offsetY += self.dt * speed
        i = 0
        for each in self.text:
            text_rect = each.get_rect(center=(320 / 2, i * 24 - self.offsetY))  # Adjust spacing dynamically
            self.window.blit(each, text_rect.topleft)
            i += 1
            if i == len(self.text) - 1 and i * 24 - self.offsetY < -30:
                self.state_machine.exit_state()


    def exit(self):
        ...