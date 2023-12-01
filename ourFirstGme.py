import pygame
from random import randint
from physics import Bird, Pipe, Score

pygame.init()

FPS = 60

#Game over event
GAME_OVER = pygame.USEREVENT + 1
def game_over(text):
    font = pygame.font.Font(SCORE_FONT, SCORE_SIZE)
    draw_text = font.render(text, 1, SCORE_COLOR)
    screen.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)
    pygame.quit()

#Font
SCORE_FONT = pygame.font.get_default_font()

#Colors
SKY_BLUE = (15, 200, 255)
BIRD_COLOR = (255, 180, 0)
PIPE_COLOR = (0, 200, 15)
SCORE_COLOR = (255, 255, 255)

#Dimensions
WIDTH, HEIGHT = 1000, 600
BIRD_WIDTH = 25
BIRD_HEIGHT = 25
PIPE_WIDTH = 80
PIPE_INNER_DISTANCE = 200
PIPE_SPACE_BETWEEN = WIDTH // 4
SCORE_SIZE = 32

#Setting game display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")


#Setting game icon
game_icon = pygame.image.load('flappyBirdIcon.png')
pygame.display.set_icon(game_icon) 

#Setting clock
clock = pygame.time.Clock()

#Setting game objects
bird = Bird(WIDTH//3, HEIGHT//2, BIRD_WIDTH, BIRD_HEIGHT, BIRD_COLOR)
score = Score(BIRD_WIDTH, BIRD_HEIGHT, SCORE_SIZE, SCORE_FONT, SCORE_COLOR)

def create_pipe(x):
    y = randint(BIRD_HEIGHT, HEIGHT - PIPE_INNER_DISTANCE - BIRD_HEIGHT)
    return [Pipe(x, 0, PIPE_WIDTH, y, PIPE_COLOR, 100 * (1 + 0.25 * score.level)), Pipe(x, y + PIPE_INNER_DISTANCE, PIPE_WIDTH, HEIGHT - y - PIPE_INNER_DISTANCE, PIPE_COLOR, 100 * (1 + 0.25 * score.level))]
pipes = []
pipes += create_pipe(WIDTH) + create_pipe(WIDTH + PIPE_SPACE_BETWEEN) + create_pipe(WIDTH + 2 * PIPE_SPACE_BETWEEN)

run = True
while run:
    clock.tick(FPS)
    screen.fill(SKY_BLUE)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == GAME_OVER:
            game_over("GAME OVER YOU SCORED " + str(score.value))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump(screen)
    
    for pipe in pipes:
        if pipe.x < -PIPE_WIDTH:
            pipes.remove(pipe)
            if len(pipes) < 6:
                pipes += create_pipe(WIDTH)

        elif (pipe.x + PIPE_WIDTH) < bird.x and not pipe.isScored:
            score.value += score.level
            pipe.isScored = True
        
        pipe.update(screen)
    
    bird.update(screen) 
    score.update(screen)

    if bird.collider.collidelist([pipe.collider for pipe in pipes]) >= 0:
        pygame.event.post(pygame.event.Event(GAME_OVER))


    pygame.display.update()

pygame.quit()