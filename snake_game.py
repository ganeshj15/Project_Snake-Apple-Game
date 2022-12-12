
import pygame as pg
from pygame.locals import *
import time
import random

size = 40
background_color = (52, 235, 192)
class Apple():
    def __init__(self,parent_screen):
        self.parent_screen = parent_screen
        self.image = pg.image.load(r"resources\apple.jpg").convert()
        self.x = size * 3
        self.y = size * 3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pg.display.flip()

    def move(self):
        self.x = random.randint(0,24) * size
        self.y = random.randint(0,14) * size



class Snake():
    def __init__(self,parent_screen):
        self.parent_screen = parent_screen
        self.block = pg.image.load(r"resources\block.jpg").convert()
        self.direction = 'up'

        self.length = 1
        self.x = [size * 12]
        self.y = [size * 6]


    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        if self.direction == 'up':   # i have taken here up instead of down
            self.y[0] -= size
        if self.direction == 'down':
            self.y[0] += size
        if self.direction == 'left':
            self.x[0] -= size
        if self.direction == 'right':
            self.x[0] += size

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pg.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)



class Game():
    def __init__(self):
        pg.init()
        pg.display.set_caption("Snake & Apple Game@GDJ")

        pg.mixer.init()
        self.play_bg_music()

        self.screen = pg.display.set_mode((1000, 600))
        self.snake = Snake(self.screen)
        self.snake.draw()
        self.apple = Apple(self.screen)
        self.apple.draw()


    def is_collisions(self,x1,y1,x2,y2):
        if x1 >= x2 and x1 < x2 + size:
            if y1 >= y2 and y1 < y2 + size:
                return True

        return False

    def display_score(self):
        font = pg.font.SysFont('tahoma',30,bold =True)
        score = font.render(f"Score: {self.snake.length}",True,(252, 186, 3))
        self.screen.blit(score,(810,10))

    def play_bg_music(self):
        pg.mixer.music.load("resources/snake_theme.mp3")
        pg.mixer.music.play(loops= -1)   # loops = -1 for playing the bg music continuously


    def add_background(self):
        image = pg.image.load("resources/background.jpg")
        self.screen.blit(image,(0,0))

    def play(self):
        self.add_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pg.display.flip()

        # snake colliding with apple
        if self.is_collisions(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            sound = pg.mixer.Sound("resources/apple_eating.mp3")
            pg.mixer.Sound.play(sound)
            self.snake.increase_length()
            self.apple.move()
            
        # snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collisions(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                sound = pg.mixer.Sound("resources/crash.mp3")
                pg.mixer.Sound.play(sound)
                raise "Game Over"
        # snake colliding with boundaries
        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 600):
            sound = pg.mixer.Sound("resources/crash.mp3")
            pg.mixer.Sound.play(sound)
            raise "Game Over"

    def show_game_over(self):
        self.add_background()
        font = pg.font.SysFont('arial', 27,italic= True)
        line1 = font.render(f" Game Over !Your Score is: {self.snake.length}",True,(252, 161, 3))
        self.screen.blit(line1,(300, 250))
        line2 = font.render("Press Enter to Play Again & Esc to exit", True, (252, 161, 3))
        self.screen.blit(line2, (300, 300))
        pg.display.flip()
        pg.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.screen)
        self.apple = Apple(self.screen)

    def run(self):
        app_running = True
        pause = False

        while app_running:
            for event in pg.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:  # used to close with escape key
                        app_running = False

                    if event.key == K_RETURN:
                        pg.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:  # QUIT event will be produced when we clicked on close option of our window.
                    app_running = False

            try:
                if not pause:
                    self.play()
            except Exception as e :
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.1)




if __name__ == "__main__":
    game = Game()
    game.run()






