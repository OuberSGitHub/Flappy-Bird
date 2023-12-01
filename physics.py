import pygame

pygame.font.init()

GRAVITY = 200
FPS = 60

clock = pygame.time.Clock()
dt = clock.tick(FPS) / 1000

class Score:
    def __init__(self, x, y, textSize, font, color):
        self.x = x
        self.y = y
        self.text_size = textSize
        self.color = color
        self.font = font
        self.value = 0
        self.level = 1

    def update(self, screen):
        font = pygame.font.Font(self.font, self.text_size)
        text = font.render("SCORE : " + str(self.value), True, self.color)
        text1 = font.render("LEVEL : " + str(self.level), True, self.color)
        screen.blit(text, (self.x, self.y))
        screen.blit(text1, (self.x, self.y + 2 + self.text_size))

        if self.value > 100 and self.level < 2:
            self.level += 1
        elif self.value > 300 and self.level < 3:
            self.level += 1
    

class Pipe:
    def __init__(self, x, y, width, height, color, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.collider = pygame.Rect(self.x, self.y, self.height, self.width)
        self.color = color
        self.isScored = False

    def change_collider(self):
        self.collider = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.x -= self.speed * dt

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.collider)

    def update(self, screen):
        self.move()
        self.change_collider()
        self.draw(screen)

class Bird:
    def __init__(self, x, y, width, height, color, speed = [0, 0]):
        self.jump_count = 0
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.collider = pygame.Rect(self.x, self.y, self.height, self.width)
        self.color = color

    def change_collider(self):
        self.collider = pygame.Rect(self.x, self.y, self.height, self.width)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.collider)

    def jump(self, screen):
        if self.jump_count <= FPS//2:
            self.jump_count = FPS//2

    def move(self):
        gravity = GRAVITY * (1 + (60 - 2 * self.jump_count)//FPS)
        self.speed[1] += (1 - 7 * self.jump_count//FPS) * gravity
        if self.jump_count > 0:
            self.jump_count -= 1

    def update(self, screen):
        self.move()
        self.y = self.speed[1] * dt
        self.change_collider()
        self.draw(screen)



    