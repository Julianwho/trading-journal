import pygame
import random

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
SPEED = 10

# Set up some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Set up the snake and food
snake = [(WIDTH // 2, HEIGHT // 2)]
food = (random.randint(0, GRID_SIZE - 1) * 20, random.randint(0, GRID_SIZE - 1) * 20)
direction = (1, 0)

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 1):
                direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1):
                direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)

    # Move the snake
    head = snake[0]
    new_head = (head[0] + direction[0] * 20, head[1] + direction[1] * 20)
    snake.insert(0, new_head)

    # Check for collisions
    if (new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT or
            new_head in snake[1:]):
        print("Game Over!")
        pygame.quit()
        sys.exit()

    # Check for food
    if snake[0] == food:
        food = (random.randint(0, GRID_SIZE - 1) * 20, random.randint(0, GRID_SIZE - 1) * 20)
    else:
        snake.pop()

    # Draw everything
    screen.fill(BLACK)
    for pos in snake:
        pygame.draw.rect(screen, WHITE, (pos[0], pos[1], 20, 20))
    pygame.draw.rect(screen, RED, (food[0], food[1], 20, 20))
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.delay(1000 // SPEED)
