import pygame, sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 1080, 540
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Bird:
    def __init__(self, x, y):
        """Initialize the bird with position, physics, and appearance."""
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100
        self.velocity = 0
        self.gravity = 1  # Gravity effect
        self.lift = -15   # Jump force
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.draw_bird()

    def draw_bird(self):
        """Draw a simple bird-like shape."""
        # Body
        pygame.draw.circle(self.surface, (255, 223, 0, 255), (50, 50), 40)
        # Wing
        pygame.draw.polygon(self.surface, (200, 200, 0, 255), [(30, 50), (10, 20), (50, 30)])
        # Beak
        pygame.draw.polygon(self.surface, (255, 150, 0, 255), [(70, 45), (90, 50), (70, 55)])
        # Eye
        pygame.draw.circle(self.surface, (255, 255, 255, 255), (60, 35), 10)
        pygame.draw.circle(self.surface, (0, 0, 0, 255), (63, 35), 5)

    def update(self):
        """Apply gravity and update bird's position."""
        self.velocity += self.gravity
        self.y += self.velocity

        # Prevent bird from falling through the ground
        if self.y + self.height > HEIGHT:
            self.y = HEIGHT - self.height
            self.velocity = 0  # Reset velocity on landing

    def jump(self):
        """Make the bird jump when space is pressed."""
        self.velocity = self.lift

    def draw(self, win):
        """Render the bird onto the screen."""
        win.blit(self.surface, (self.x, self.y))

# Create a bird instance
bird = Bird(300, 100)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()  # Jump when space is pressed

    # Update game state
    bird.update()
    
    # Clear screen and redraw
    window.fill((255, 255, 255))
    bird.draw(window)
    
    # Update display and limit FPS
    pygame.display.flip()
    clock.tick(30)