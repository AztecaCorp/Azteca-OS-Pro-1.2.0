import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 600, 400
FPS = 60
PLAYER_WIDTH, PLAYER_HEIGHT = 60, 20
OBJECT_WIDTH, OBJECT_HEIGHT = 20, 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Falling Object")

# Set up font
font = pygame.font.SysFont("Arial", 24)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - PLAYER_HEIGHT // 2)

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += 5
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.x += 5

# Falling object class
class FallingObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((OBJECT_WIDTH, OBJECT_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - OBJECT_WIDTH)
        self.rect.y = -OBJECT_HEIGHT

    def update(self):
        self.rect.y += 5
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - OBJECT_WIDTH)
            self.rect.y = -OBJECT_HEIGHT

# Initialize game objects
player = Player()
player_group = pygame.sprite.Group(player)
falling_objects_group = pygame.sprite.Group()
all_sprites_group = pygame.sprite.Group(player)

# Add some falling objects
for _ in range(5):
    falling_object = FallingObject()
    falling_objects_group.add(falling_object)
    all_sprites_group.add(falling_object)

# Score and game over flag
score = 0
game_over = False

# Game loop
clock = pygame.time.Clock()
while True:
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Game logic
    if not game_over:
        keys = pygame.key.get_pressed()
        player_group.update(keys)
        falling_objects_group.update()

        # Check for collisions
        for obj in falling_objects_group:
            if player.rect.colliderect(obj.rect):
                obj.rect.x = random.randint(0, WIDTH - OBJECT_WIDTH)
                obj.rect.y = -OBJECT_HEIGHT
                score += 1

        # Check if the player misses an object (falls off screen)
        for obj in falling_objects_group:
            if obj.rect.top > HEIGHT:
                game_over = True

    # Draw everything
    all_sprites_group.draw(screen)

    # Display score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Display game over message
    if game_over:
        game_over_text = font.render("Game Over! Press Q to Quit", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))

    # Update display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(FPS)
