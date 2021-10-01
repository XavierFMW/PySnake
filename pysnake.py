from random import randint
import pygame
import math
import sys

WINDOW_WIDTH, WINDOW_HEIGHT = 1300, 700  
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("PySnake")


class segment:

    def __init__(self, properties=None, next=None):

        self.next = next

        if properties == None:
            self.rect = pygame.Rect(next.rect.x, next.rect.y, next.rect.width, next.rect.height)

        else:
            self.rect = pygame.Rect(properties[0], properties[1], properties[2], properties[3])


class player:

    def __init__(self):

        self.direction = 1

        # Directions
        #
        # 0 = Down
        # 1 = Right
        # 2 = Up
        # 3 = Left

        self.size = 50
        self.speed = self.size

        self.image = pygame.transform.scale(pygame.image.load("C:\\Users\\xavif\\Desktop\\Storage\\Projects\\Portfolio\\PySnake\\player.png"), (self.size, self.size))
        self.apple_image = pygame.transform.scale(pygame.image.load("C:\\Users\\xavif\\Desktop\\Storage\\Projects\\Portfolio\\PySnake\\apple.png"), (self.size, self.size))
        self.empty = pygame.transform.scale(pygame.image.load("C:\\Users\\xavif\\Desktop\\Storage\\Projects\\Portfolio\\PySnake\\empty.png"), (self.size, self.size))
        self.button_image = pygame.transform.scale(pygame.image.load("C:\\Users\\xavif\\Desktop\\Storage\\Projects\\Portfolio\\PySnake\\button.png"), (800, 100))

        self.head = segment((200, 350, self.size, self.size))
        self.body = segment((150, 350, self.size, self.size), self.head)
        self.tail = segment((100, 350, self.size, self.size), self.body)

        self.segments = [self.tail, self.body, self.head]
        self.apple = pygame.Rect(800, 350, self.size, self.size)

        self.ingame = False
        self.score = 0
        self.highscore = 0

    
    def move(self):

        body = self.segments

        last_segment = body[0]

        body.pop(0)
        body.insert(len(body) - 1, last_segment)

        last_segment.next = body[-1]
        body[-3].next = body[-2]

        last_segment.rect.x = last_segment.next.rect.x
        last_segment.rect.y = last_segment.next.rect.y


def game_over(snake):

    mouse_over = 0

    clock = pygame.time.Clock()
    fps = 10
    
    if snake.score > snake.highscore:
        snake.highscore = snake.score

    window.fill((0, 0, 0))
    
    title_font = pygame.font.Font("C:\\Users\\xavif\\Desktop\\Storage\\Projects\\Portfolio\\PySnake\\8bit.TTF", 75) 
    title = title_font.render("GAME OVER", False, (255, 255, 255))
    window.blit(title, (math.floor((WINDOW_WIDTH / 2) - 350), math.floor(WINDOW_HEIGHT / 5.142)))

    score_font = pygame.font.Font("C:\\Users\\xavif\\Desktop\\Storage\\Projects\\Portfolio\\PySnake\\8bit.TTF", 30) 
    score_text = score_font.render(f"Score  {snake.score}", False, (255, 255, 255))
    window.blit(score_text, (math.floor(WINDOW_WIDTH / 2.46), math.floor(WINDOW_HEIGHT / 3.1)))

    highscore_text = score_font.render(f"Highscore  {snake.highscore}", False, (255, 255, 255))
    window.blit(highscore_text, (math.floor(WINDOW_WIDTH / 2.46), math.floor(WINDOW_HEIGHT / 2.6))) #585, 325

    BUTTON_WIDTH = 800
    BUTTON_HEIGHT = 100
    BUTTON_X = math.floor((WINDOW_WIDTH / 2) - (BUTTON_WIDTH / 2))

    button1 = pygame.Rect(BUTTON_X, math.floor(WINDOW_HEIGHT / 2.25), BUTTON_WIDTH, BUTTON_HEIGHT)
    button2 = pygame.Rect(BUTTON_X, math.floor(WINDOW_HEIGHT / 1.5), BUTTON_WIDTH, BUTTON_HEIGHT)

    button_font = pygame.font.Font("C:\\Users\\xavif\\Desktop\\Storage\\Projects\\Portfolio\\PySnake\\8bit.TTF", 40)

    window.blit(snake.button_image, (button1.x, button1.y))
    window.blit(snake.button_image, (button2.x, button2.y))

    button1_text = button_font.render("Play", False, (0, 0, 0))
    window.blit(button1_text, (math.floor(WINDOW_WIDTH / 2.2), math.floor(WINDOW_HEIGHT / 2.11)))

    button2_text = button_font.render("Exit", False, (0, 0, 0))
    window.blit(button2_text, (math.floor(WINDOW_WIDTH / 2.2), math.floor(WINDOW_HEIGHT / 1.44)))
        
    pygame.display.update()

    snake.ingame = False
    while not snake.ingame:
        clock.tick(fps)

        mx, my = pygame.mouse.get_pos()
        print(pygame.mouse.get_pos())

        if button1.collidepoint((mx, my)):
            mouse_over = 1
        elif button2.collidepoint((mx, my)):
            mouse_over = 2
        else:
            mouse_over = 0

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

                if event.key == pygame.K_RETURN:
                    snake.ingame = True

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1 and mouse_over == 1:
                    snake.ingame = True
                elif event.button == 1 and mouse_over == 2:
                    pygame.quit()

    snake.score = 0
    snake.direction = 1
    snake.head.rect.x, snake.head.rect.y = 200, 350
    snake.segments = [snake.tail, snake.body, snake.head]

    window.fill((0, 0, 0))
    game(snake, clock, fps)


def character_movement(snake):
    
    snake.move()
    
    if snake.direction == 0:  # Down
        snake.head.rect.y += snake.speed
    
    elif snake.direction == 1:  # Right
        snake.head.rect.x += snake.speed
    
    elif snake.direction == 2:  # Up
        snake.head.rect.y -= snake.speed
    
    else:  # Left
        snake.head.rect.x -= snake.speed


def make_apple(snake):
    
    x = randint(0, (WINDOW_WIDTH // snake.size) - 1) * snake.size
    y = randint(0, (WINDOW_HEIGHT // snake.size) - 1) * snake.size

    snake.apple = pygame.Rect(x, y, snake.size, snake.size)

    for segment in snake.segments:

        if segment.rect.colliderect(snake.apple):
            make_apple(snake)


def add_segment(snake):
    snake.segments.insert(0, segment(next=snake.segments[0]))


def character_collision(snake):

    for segment in snake.segments[:-2]:

        if snake.head.rect.colliderect(segment.rect):
            game_over(snake)

    if (snake.head.rect.x == 0 and snake.direction == 3 or snake.head.rect.x == WINDOW_WIDTH and snake.direction == 1 or 
    snake.head.rect.y  == 0 and snake.direction == 2 or (snake.head.rect.y + snake.head.rect.height) == WINDOW_HEIGHT and snake.direction == 0):

        game_over(snake)

    if snake.head.rect.colliderect(snake.apple):
        
        snake.score += 1
        add_segment(snake)
        make_apple(snake)


def game(snake, clock, fps):

    tail_coords = (0, 0)

    while True:
        clock.tick(fps)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    sys.exit()

                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and snake.direction != 2:
                    snake.direction = 0
                
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and snake.direction != 3:
                    snake.direction = 1
                
                elif (event.key == pygame.K_UP or event.key == pygame.K_w) and snake.direction != 0:
                    snake.direction = 2
                
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and snake.direction != 1:
                    snake.direction = 3


        character_collision(snake)
        character_movement(snake)
        
        window.blit(snake.apple_image, (snake.apple.x, snake.apple.y))
        window.blit(snake.image, (snake.head.rect.x, snake.head.rect.y))
        window.blit(snake.empty, tail_coords)

        tail = snake.segments[0]
        tail_coords = (tail.rect.x, tail.rect.y)

        pygame.display.update()


def main_menu():

    snake = player()
    clock = pygame.time.Clock()
    fps = 10

    mouse_over = 0

    window.fill((0, 0, 0))

    pygame.font.init()
    title_font = pygame.font.Font("C:\\Users\\xavif\\Desktop\\Storage\\Projects\\Portfolio\\PySnake\\8bit.TTF", 75) 
    title = title_font.render("PySnake", False, (255, 255, 255))
    window.blit(title, (math.floor((WINDOW_WIDTH / 2) - 230), math.floor(WINDOW_HEIGHT / 5.142)))

    BUTTON_WIDTH = 800
    BUTTON_HEIGHT = 100
    BUTTON_X = math.floor((WINDOW_WIDTH / 2) - (BUTTON_WIDTH / 2))

    button1 = pygame.Rect(BUTTON_X, math.floor(WINDOW_HEIGHT / 2.25), BUTTON_WIDTH, BUTTON_HEIGHT)
    button2 = pygame.Rect(BUTTON_X, math.floor(WINDOW_HEIGHT / 1.5), BUTTON_WIDTH, BUTTON_HEIGHT)

    button_font = pygame.font.Font("C:\\Users\\xavif\\Desktop\\Storage\\Projects\\Portfolio\\PySnake\\8bit.TTF", 40)

    window.blit(snake.button_image, (button1.x, button1.y))
    window.blit(snake.button_image, (button2.x, button2.y))

    button1_text = button_font.render("Play", False, (0, 0, 0))
    window.blit(button1_text, (math.floor(WINDOW_WIDTH / 2.2), math.floor(WINDOW_HEIGHT / 2.11)))

    button2_text = button_font.render("Exit", False, (0, 0, 0))
    window.blit(button2_text, (math.floor(WINDOW_WIDTH / 2.2), math.floor(WINDOW_HEIGHT / 1.44)))
        
    pygame.display.update()

    while not snake.ingame:
        clock.tick(fps)

        mx, my = pygame.mouse.get_pos()

        if button1.collidepoint((mx, my)):
            mouse_over = 1
        elif button2.collidepoint((mx, my)):
            mouse_over = 2
        else:
            mouse_over = 0

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

                if event.key == pygame.K_RETURN:
                    snake.ingame = True

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1 and mouse_over == 1:
                    snake.ingame = True
                elif event.button == 1 and mouse_over == 2:
                    pygame.quit()

    window.fill((0, 0, 0))
    game(snake, clock, fps)


main_menu()
