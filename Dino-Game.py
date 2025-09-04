import pygame
import sys
import os

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino-Game")

# Clock
clock = pygame.time.Clock()
FPS = 60

# Fonts
font = pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Arial", 48)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GROUND_COLOR = (83, 83, 83)

# Load images (fallback to None if not available)
def load_img(name, scale=None):
    if os.path.exists(name):
        img = pygame.image.load(name).convert_alpha()
        if scale:
            img = pygame.transform.scale(img, scale)
        return img
    return None

# Try to load Dino + cactus
dino_img = load_img("Dinosasur.png", (60, 60))
cactus_img = load_img("cactus.png", (40, 60))
ground_height = 50

# Dino properties
dino_width, dino_height = 60, 60
dino_x = 100
dino_y = HEIGHT - dino_height - ground_height
dino_vel_y = 0
gravity = 1
is_jumping = False

# Obstacle properties
obstacle_width, obstacle_height = 40, 60
obstacle_x = WIDTH + 200
obstacle_y = HEIGHT - obstacle_height - ground_height
obstacle_speed = 7

# Ground scrolling
ground_x = 0

# Score
score = 0

# Game states
game_active = False
game_over = False


def reset_game():
    global dino_y, dino_vel_y, is_jumping, obstacle_x, score, game_over, game_active, ground_x, obstacle_speed
    dino_y = HEIGHT - dino_height - ground_height
    dino_vel_y = 0
    is_jumping = False
    obstacle_x = WIDTH + 200
    obstacle_speed = 7
    score = 0
    ground_x = 0
    game_over = False
    game_active = True


# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not game_active and not game_over:
                if event.key == pygame.K_SPACE:
                    reset_game()
            elif game_active:
                if event.key == pygame.K_SPACE and not is_jumping:
                    dino_vel_y = -15
                    is_jumping = True
            elif game_over:
                if event.key == pygame.K_SPACE:
                    reset_game()

    if game_active:
        # --- Game Logic ---
        # Dino movement
        dino_y += dino_vel_y
        dino_vel_y += gravity

        if dino_y >= HEIGHT - dino_height - ground_height:
            dino_y = HEIGHT - dino_height - ground_height
            is_jumping = False

        # Obstacle movement
        obstacle_x -= obstacle_speed
        if obstacle_x < -obstacle_width:
            obstacle_x = WIDTH
            score += 1
            obstacle_speed += 0.2

        # Rectangles
        dino_rect = pygame.Rect(dino_x, dino_y, dino_width, dino_height)
        obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)

        # Collision detection
        if dino_rect.colliderect(obstacle_rect):
            game_active = False
            game_over = True

        # --- Draw ---
        # Ground scrolling
        ground_x -= obstacle_speed
        if ground_x <= -WIDTH:
            ground_x = 0
        pygame.draw.rect(screen, GROUND_COLOR, (ground_x, HEIGHT-ground_height, WIDTH, ground_height))
        pygame.draw.rect(screen, GROUND_COLOR, (ground_x+WIDTH, HEIGHT-ground_height, WIDTH, ground_height))

        # Dino
        if dino_img:
            screen.blit(dino_img, (dino_x, dino_y))
        else:
            pygame.draw.rect(screen, (50, 200, 50), dino_rect)

        # Cactus
        if cactus_img:
            screen.blit(cactus_img, (obstacle_x, obstacle_y))
        else:
            pygame.draw.rect(screen, (0, 150, 0), obstacle_rect)

        # Score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

    elif not game_active and not game_over:
        # --- Start Screen ---
        title_text = big_font.render("    Dino-Game", True, BLACK)
        start_text = font.render(" Press SPACE to Start", True, BLACK)
        screen.blit(title_text, (WIDTH//2 - 150, HEIGHT//2 - 50))
        screen.blit(start_text, (WIDTH//2 - 120, HEIGHT//2 + 20))

    elif game_over:
        # --- Game Over Screen ---
        over_text = big_font.render("GAME OVER", True, BLACK)
        score_text = font.render(f"Final Score: {score}", True, BLACK)
        restart_text = font.render("  Press SPACE to Restart", True, BLACK)
        screen.blit(over_text, (WIDTH//2 - 120, HEIGHT//2 - 60))
        screen.blit(score_text, (WIDTH//2 - 80, HEIGHT//2))
        screen.blit(restart_text, (WIDTH//2 - 150, HEIGHT//2 + 40))

    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
