import pygame, sys, random

pygame.init()
sound_player_die = pygame.mixer.Sound("Sounds/Game_over.wav")
sound_paddle_hit = pygame.mixer.Sound("Sounds/Paddle_hit.wav")
sound_screen_hit = pygame.mixer.Sound("Sounds/Ball_collition.wav")
sound_level_up = pygame.mixer.Sound("Sounds/Level_up.wav")

def ball_movement():

    global ball_speed_x, ball_speed_y, score, start

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Start the ball movement when the game begins
    # TODO Task 5 Create a Merge Conflict
    speed = 7
    if start:
        ball_speed_x = speed * random.choice((1, -1))  # Randomize initial horizontal direction
        ball_speed_y = speed * random.choice((1, -1))  # Randomize initial vertical direction
        start = False

    # Ball collision with the player paddle
    if ball.colliderect(player):
        if abs(ball.bottom - player.top) < 10:  # Check if ball hits the top of the paddle
            # Score (Fixed)
            score += 1  # Increase player score
            ball_speed_y *= -1  # Reverse ball's vertical direction
            sound_paddle_hit.play()

    # Ball collision with top boundary
    if ball.top <= 0:
        ball_speed_y *= -1  # Reverse ball's vertical direction
        sound_screen_hit.play()

    # Ball collision with left and right boundaries
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x *= -1
        sound_screen_hit.play()

    # Ball goes below the bottom boundary (missed by player)
    if ball.bottom > screen_height:
        restart()  # Reset the game

def player_movement():
    """
    Handles the movement of the player paddle, keeping it within the screen boundaries.
    """
    player.x += player_speed  # Move the player paddle horizontally

    # Prevent the paddle from moving out of the screen boundaries
    if player.left <= 0:
        player.left = 0
    if player.right >= screen_width:
        player.right = screen_width

def restart():
    """
    Resets the ball and player scores to the initial state.
    """
    global ball_speed_x, ball_speed_y, score
    ball.center = (screen_width / 2, screen_height / 2)  # Reset ball position to center
    ball_speed_y, ball_speed_x = 0, 0  # Stop ball movement
    score = 0  # Reset player score

# General setup
pygame.mixer.pre_init(44100, -16, 1, 1024)
pygame.init()
clock = pygame.time.Clock()

# Main Window setup
screen_width = 500  # Screen width (can be adjusted)
screen_height = 500  # Screen height (can be adjusted)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')  # Set window title

# Game Rectangles (ball and player paddle)
ball = pygame.Rect(screen_width / 2 - 10, screen_height / 2 - 10, 20, 20)  # Ball (centered)
# TODO Task 1 Make the paddle bigger
player_height = 478
player_width = 208
player = pygame.Rect(screen_width/2 - 45, screen_height - 20, player_width, player_height)  # Player paddle

# Game Variables
ball_speed_x = 0
ball_speed_y = 0
player_speed = 0
speed = 6

# Score Text setup
score = 0
basic_font = pygame.font.Font('freesansbold.ttf', 28)  # Font for displaying score

start = False  # Indicates if the game has started
previous_level = None

# Main game loop
while True:
    # Event handling
    # TODO Task 4: Add your name
    name = "Fabian Ortiz"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quit the game
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_speed -= 6  # Move paddle left
            if event.key == pygame.K_RIGHT:
                player_speed += 6  # Move paddle right
            if event.key == pygame.K_SPACE:
                start = True  # Start the ball movement
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_speed += 6  # Stop moving left
            if event.key == pygame.K_RIGHT:
                player_speed -= 6  # Stop moving right

    # Game Logic
    ball_movement()
    player_movement()

    # Visuals
    bg_color = pygame.Color('grey12')
    light_green = pygame.Color('green')
    light_grey = pygame.Color('grey100')
    screen.fill(bg_color)  # Clear screen with background color
    pygame.draw.rect(screen, light_grey, player)  # Draw player paddle
    pygame.draw.ellipse(screen, light_green, ball)  # Draw ball
    player_text = basic_font.render(f'{score}', False, light_grey)  # Render player score
    screen.blit(player_text, (screen_width / 2 - 15, 10))  # Display score on screen

    # Colors
    light_green = pygame.Color('green')
    light_yellow = pygame.Color('yellow')
    light_grey = pygame.Color('gray100')
    light_orange = pygame.Color('orange')
    red = pygame.Color('red')
    black = pygame.Color('black')

#Velocidades para niveles
    if ball_speed_x > 0:
        ball_speed_x = speed
    else:
        ball_speed_x = -speed
    if ball_speed_y > 0:
        ball_speed_y = speed
    else:
        ball_speed_y = -speed
    #Levels


    if score <= 9:
        difficulty = "Easy"
        pygame.draw.ellipse(screen, light_green, ball)
        speed = 6
        player.width = 208
    elif 19 >= score >= 10:
        difficulty = "Normal"
        pygame.draw.ellipse(screen, light_yellow, ball)
        speed = 7
        player.width = 150
    elif 29 >= score >= 20:
        difficulty = "Medium"
        pygame.draw.ellipse(screen, light_orange, ball)
        speed = 9
        player.width = 140
    elif 39 >= score >= 30:
        difficulty = "Hard"
        pygame.draw.ellipse(screen, red, ball)
        speed = 12
        player.width = 130
    elif score >= 40:
        difficulty = "Imposible 💀"
        pygame.draw.ellipse(screen, black, ball)
        speed = 14
        player.width = 120

    difficulty_text = basic_font.render(f'{difficulty}', False, light_grey)
    screen.blit(difficulty_text, (10, 10))

    if difficulty != previous_level:
        sound_level_up.play()
        previous_level = difficulty

    def restart():
        global ball_speed_x, ball_speed_y, score, speed, player
        ball.center = (screen_width / 2, screen_height / 2)
        ball_speed_y, ball_speed_x = 0, 0
        score = 0
        speed = 6
        player.width = 208
        player.height = 20
        player.x = (screen_width - player.width) // 2
        player.y = screen_height - player.height - 10
        sound_player_die.play()

    # Update display
    pygame.display.flip()
    clock.tick(60)  # Maintain 60 frames per second