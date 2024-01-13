# Import Pygame and system modules

# pygame provides a simple and easy-to-use interface for creating multimedia applications, including games.
# Graphics: loading images, drawing shapes and text, and handling animation.
# input: Handling keyboard, mouse, and joystick input. 
# Events: Handling events such as key presses, mouse clicks, and wnidow events. 
import pygame
# sys provides access to system-specific parameters and functions. 
import sys
# random provides acess to a variety of pseudo-random number generators. 
import random

# initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
# Frames Per Second: frame rate for the game. It means that the game aims to update and render 60 frames every second. 
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fighter Jet Game")

# Load images
player_image = pygame.image.load("fighter_jet02.png")
enemy_image = pygame.image.load("enemy_jet02.png")
bullet_image = pygame.image.load("bullet02.png")

# Set up the player
player_rect = player_image.get_rect() # get the rectangular area of a surface (such as an image). 
player_rect.centerx = WIDTH // 2 # horizontal center
player_rect.bottom = HEIGHT - 20 # player character positioned bottom and 20 pixels from the bottom. 
player_speed = 5 # speed at which the player can move horizontally. 

# Set up the enemies
enemies = [] # empty list and store  information. 
enemy_speed = 5 # speed at which enemy objects will move, 
enemy_spawn_timer = 0 # keep spawning the enemy, one by one,
enemy_spawn_interval = 60 # spawning remdering between enemy,

# Set up the bullets
bullets = [] # empty list
bullet_speed = 7 # speed at which the bullet move in the game,

# Set up the fonts
font = pygame.font.Font(None, 36) # handling fonts in game development, None=default, size=36pixels,

# Display start dcreen text
start_text = font.render("Press SPACE to Start", True, WHITE) # True enables antialiasing, smothens the edges of the text. 
start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))# gets the rectangular area of the rendered text, and center coordinates,

# Display game over screen text
game_over_text = font.render("Game Over! Press R to Retry", True, WHITE)
game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Set up the clock
# control the speed of the game loop and ensures that the game runs at a consistent frame rate. 
clock = pygame.time.Clock()

# Function to initialize game state
def start_game():
    global player_rect, enemies, bullets, game_over, bullet_enemy_collisions # global applies on full program inside and outside,
    player_rect.centerx = WIDTH // 2 
    player_rect.bottom = HEIGHT - 20
    enemies = []
    bullets = []
    game_over = False
    bullet_enemy_collisions = 0
    
# game state variables
game_running = False
game_over = False
bullet_enemy_collisions = 0

# Main loop for the start screen
while not game_running:
    for event in pygame.event.get():
        # Check for quit event
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Check for key press event
        elif event.type == pygame.KEYDOWN:
            # Check if SPACE key is pressed
            if event.key == pygame.K_SPACE:
                # Start the game
                start_game()
                game_running = True
    
    # Dislay start screen        
    screen.fill(BLACK)
    screen.blit(start_text, start_rect)
    pygame.display.flip() # update the display after making changes. 
    clock.tick(FPS)

# Main game loop
while True: 
    for event in pygame.event.get():
        # Check for the quit event
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Check for key press event
        elif event.type == pygame.KEYDOWN:
            # Check if the game is not over
            if not game_over:
                # Check if SPACE key is pressed and shooting is enabled
                if event.key == pygame.K_UP: 
                    # Shoot a bullet
                    bullet_rect = bullet_image.get_rect()
                    bullet_rect.centerx = player_rect.centerx
                    bullet_rect.bottom = player_rect.top
                    bullets.append(bullet_rect)
            # For quit game pressed key ESCAPE
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            # Check if R key is pressed during game over
            elif game_over and event.key == pygame.K_r:
                # Restart the game
                start_game()
                game_over = False
    
    if not game_over:  
        # Player movement          
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0: # didn't move outside the scrren,
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
            player_rect.x += player_speed
        
        # Enemy spawning
        if enemy_spawn_timer == 0:
            enemy_rect = enemy_image.get_rect()
            enemy_rect.x = random.randint(0, WIDTH - enemy_rect.width) # random position within horizontal bounds,
            enemy_rect.y = -enemy_rect.height # position above the screen, effectively placing it just outside the top edge of the screen,
            enemies.append(enemy_rect) # nemly created enemy rectangle is added to the enemies list,
            enemy_spawn_timer = enemy_spawn_interval
        else:
            # ensures that the next enemy will be spawned only after a certain number of iterations through the game loop,
            enemy_spawn_timer -= 1
        
        # Update enemy positions
        for enemy in enemies:
            enemy.y += enemy_speed # moves each enemy down the screen.
        
        # Update bullet positions
        for bullet in bullets:
            bullet.y -= bullet_speed # moves each bullet upward,
        
        # Collision deection - bullets and eb=nemies    
        for bullet in bullets:
            for enemy in enemies:
                if bullet.colliderect(enemy):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    bullet_enemy_collisions += 1
        
        # Collision detection -player and enemies    
        for enemy in enemies:
            if player_rect.colliderect(enemy):
                game_over = True
        
        # Draw everything        
        screen.fill(BLACK)
        screen.blit(player_image, player_rect)
        for enemy in enemies:
            screen.blit(enemy_image, enemy)
        for bullet in bullets:
            screen.blit(bullet_image, bullet)
        
        # Render bullet-enemy collision count    
        collision_text = font.render(f"Collisions: {bullet_enemy_collisions}", True, WHITE)
        screen.blit(collision_text, (10, 10))
    # Update the display
    if game_over:
        screen.blit(game_over_text, game_over_rect)    
    pygame.display.flip()
    
    # Remove enemies that have moved off the screen
    enemies = [enemy for enemy in enemies if enemy.y < HEIGHT]
    
    # Cap the frame rate
    clock.tick(FPS)
    