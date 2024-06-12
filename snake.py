import pygame 
import time
import random 
from pygame.math import Vector2
pygame.font.init()
FONT=pygame.font.SysFont("comicsans",30)
cell_size=28
cell_number=22
win=pygame.display.set_mode((cell_size*cell_number,cell_size*cell_number))
bg=pygame.transform.scale(pygame.image.load("backgrounds/snakebg.jpg"),(cell_size*cell_number,cell_size*cell_number))
class FRUIT:
    def __init__(self):
        self.randomize()
    def draw_fruit(self):
        self.urfruit=pygame.Rect(self.x*cell_size,self.y*cell_size,cell_size-10,cell_size-10)
        pygame.draw.rect(win,"red",self.urfruit)
    def randomize(self):
        self.x=random.randint(0,cell_number-1)
        self.y=random.randint(0,cell_number-1)
        self.pos=Vector2(self.x,self.y)
class SNAKE:
    def __init__(self):
        self.body=[Vector2(10,10),Vector2(9,10),Vector2(8,10)]
        self.direction=Vector2(1,0)
        self.hit=False
    def draw_snake(self):
        for snk in self.body:
            self.snake=pygame.Rect(snk.x*cell_size,snk.y*cell_size,cell_size,cell_size)
            pygame.draw.rect(win,"forestgreen",self.snake)
    def move_snake(self):
         self.copy=self.body[:-1]
         self.copy.insert(0,self.body[0]+self.direction)
         self.body=self.copy[:]
    def adder(self):
        self.body.append(self.body[-1]+self.direction)
    def loser(self):
        xal=self.body[0]
        for xnx in self.body[1:]:
            if xal==xnx:
                self.hit=True
                
class ELEMENTS:
    def __init__(self):
        self.fruit=FRUIT()
        self.snake=SNAKE()
    def uptodater(self):
        self.snake.move_snake()
        self.detect_collision()
        self.snake.loser()
    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
    def detect_collision(self):
        if self.snake.body[0]==self.fruit.pos:
            self.fruit.randomize()
            self.snake.adder()
def endscreen():
    image_width=cell_size*3
    image_height=cell_size*3
    global playagain_image,quitt_image
    toul=cell_size*cell_number
    gameover=FONT.render("game over !",1,"black")
    win.blit(gameover,(toul/2-gameover.get_width()/2,toul/2-gameover.get_width()/2-30))
    playagain=pygame.transform.scale(pygame.image.load("backgrounds/playagain.png"),(cell_size*3,cell_size*3))
    quitt=pygame.transform.scale(pygame.image.load("backgrounds/qui.png"),(cell_size*3,cell_size*3))
    playagain_image=playagain.get_rect(topleft=(toul/2-image_width/2-50,toul/2-image_height/2))
    win.blit(playagain,(toul/2-image_width/2-50,toul/2-image_height/2))
    win.blit(quitt,(toul/2-image_width/2+50,toul/2-image_height/2))
    pygame.display.update()
screen=pygame.USEREVENT
pygame.time.set_timer(screen,70)
def main():
    pause=False
    run=True
    hit=False
    moving=False
    elements=ELEMENTS()
    while run:
        if pause:
            pausetxt=FONT.render("game paused",1,"black")
            win.blit(pausetxt,((cell_size*cell_number)/2-pausetxt.get_width()/2,(cell_size*cell_number)/2-pausetxt.get_height()/2))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
                    run=False
                    break
                if event.type==pygame.KEYDOWN:
                    pause=False
        else:
            win.blit(bg,(0,0))
            for event in pygame.event.get():
                if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
                    run=False
                    break
                if event.type==pygame.KEYDOWN and event.key==pygame.K_p:
                    pause=True
                if event.type==screen and moving:
                    elements.uptodater()
                    if elements.snake.hit==True or (elements.snake.body[0].x<0) or (elements.snake.body[0].x>cell_number-1) or (elements.snake.body[0].y<0) or (elements.snake.body[0].y>cell_number-1):
                        endscreen()
                        choice=True
                        while choice:
                            for event in pygame.event.get():
                                if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
                                    choice=False
                                    run=False
                                    break
                                if event.type==pygame.KEYDOWN:
                                    if event.key==pygame.K_RETURN:
                                        main()
                                        choice=False
                                if event.type==pygame.MOUSEBUTTONDOWN:
                                    mouse=event.pos
                                    if playagain_image.collidepoint(mouse):
                                        main()
                                        choice=False
                                    if quitt_image.collidepoint(mouse):
                                        run=False
                                        choice=False
                                        break
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_UP and elements.snake.direction!=(0,1):
                        elements.snake.direction=Vector2(0,-1)
                        moving=True
                    if event.key==pygame.K_DOWN and elements.snake.direction!=(0,-1):
                        elements.snake.direction=Vector2(0,1)
                        moving=True
                    if event.key==pygame.K_LEFT and elements.snake.direction!=(1,0):
                        elements.snake.direction=Vector2(-1,0)
                        moving=True
                    if event.key==pygame.K_RIGHT and elements.snake.direction!=(-1,0):
                        elements.snake.direction=Vector2(1,0)
                        moving=True
            elements.draw_elements()
            pygame.display.update()
    pygame.quit()
    SystemExit
main()