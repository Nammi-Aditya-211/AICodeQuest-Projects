
import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 900, 350
GROUND_Y = 280
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chrome Dino Game")

clock = pygame.time.Clock()
FONT = pygame.font.SysFont("consolas", 22)
BIG_FONT = pygame.font.SysFont("consolas", 36, bold=True)

# Colors
WHITE = (255, 255, 255)
BLACK = (35, 35, 35)
GRAY = (150, 150, 150)
GREEN = (70, 160, 70)

# Dino settings
DINO_X = 70
DINO_W = 40
DINO_H = 48
GRAVITY = 0.8
JUMP_POWER = -14

# Game variables
dino_y = GROUND_Y - DINO_H
velocity_y = 0
obstacles = []
spawn_timer = 0
score = 0
speed = 7
game_over = False
started = False

def reset_game():
    global dino_y, velocity_y, obstacles
    global spawn_timer, score, speed, game_over, started

    dino_y = GROUND_Y - DINO_H
    velocity_y = 0
    obstacles = []
    spawn_timer = 0
    score = 0
    speed = 7
    game_over = False
    started = True

def draw_dino(x, y):
    # Body
    pygame.draw.rect(screen, BLACK, (x, y, DINO_W, DINO_H))

    # Head details
    pygame.draw.rect(screen, WHITE, (x + 26, y + 8, 5, 5))

    # Legs
    if abs(velocity_y) < 1 and not game_over:
        leg_offset = (pygame.time.get_ticks() // 100) % 2 * 5
    else:
        leg_offset = 0

    pygame.draw.rect(
        screen, BLACK,
        (x + 5, y + DINO_H - 2, 10, 9 - leg_offset // 2)
    )
    pygame.draw.rect(
        screen, BLACK,
        (x + 25, y + DINO_H - 2, 10, 9 - (5 - leg_offset) // 2)
    )

def draw_cactus(x, height):
    # Cactus trunk
    pygame.draw.rect(
        GREEN, (x, GROUND_Y - height, 18, height)
    )

    # Cactus arms
    if height > 30:
        pygame.draw.rect(
            GREEN, (x - 8, GROUND_Y - height + 15, 8, 6)
        )
        pygame.draw.rect(
            GREEN, (x + 14, GROUND_Y - height + 25, 8, 6)
        )

def show_text(text, font, color, x, y, center=True):
    image = font.render(text, True, color)
    rect = image.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(image, rect)

# Main game loop
while True:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if not started:
                reset_game()

            elif game_over:
                if event.key in (pygame.K_SPACE, pygame.K_r):
                    reset_game()

            elif event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                if dino_y >= GROUND_Y - DINO_H - 1:
                    velocity_y = JUMP_POWER

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not started or game_over:
                reset_game()
            elif dino_y >= GROUND_Y - DINO_H - 1:
                velocity_y = JUMP_POWER

    # Background
    screen.fill(WHITE)

    # Ground
    pygame.draw.line(
        screen, GRAY, (0, GROUND_Y), (WIDTH, GROUND_Y), 2
    )

    if started and not game_over:
        # Dino physics
        velocity_y += GRAVITY
        dino_y += velocity_y

        if dino_y >= GROUND_Y - DINO_H:
            dino_y = GROUND_Y - DINO_H
            velocity_y = 0

        # Spawn obstacles
        spawn_timer += 1
        if spawn_timer > random.randint(55, 95):
            height = random.choice([30, 40, 48, 55])
            obstacles.append({
                "x": WIDTH + 10,
                "height": height,
                "width": 18
            })
            spawn_timer = 0

        # Move obstacles
        for obstacle in obstacles:
            obstacle["x"] -= speed

        obstacles = [
            obs for obs in obstacles
            if obs["x"] + obs["width"] > 0
        ]

        # Score and difficulty
        score += 1
        speed = min(7 + score / 500, 15)

        # Collision detection
        dino_rect = pygame.Rect(
            DINO_X + 5, int(dino_y) + 4,
            DINO_W - 10, DINO_H - 5
        )

        for obstacle in obstacles:
            cactus_rect = pygame.Rect(
                int(obstacle["x"]),
                GROUND_Y - obstacle["height"],
                obstacle["width"],
                obstacle["height"]
            )

            if dino_rect.colliderect(cactus_rect):
                game_over = True

    # Draw objects
    draw_dino(DINO_X, int(dino_y))

    for obstacle in obstacles:
        draw_cactus(obstacle["x"], obstacle["height"])

    # Score display
    show_text(f"SCORE: {score // 6:05d}", FONT, BLACK, WIDTH - 180, 20)

    if not started:
        show_text("CHROME DINO", BIG_FONT, BLACK, WIDTH // 2, 110)
        show_text("Press SPACE or click to start", FONT, GRAY,
                  WIDTH // 2, 165)

    elif game_over:
        show_text("GAME OVER", BIG_FONT, BLACK, WIDTH // 2, 120)
        show_text(f"Final Score: {score // 6}", FONT, BLACK,
                  WIDTH // 2, 165)
        show_text("Press R or SPACE to restart", FONT, GRAY,
                  WIDTH // 2, 205)

    pygame.display.flip()
