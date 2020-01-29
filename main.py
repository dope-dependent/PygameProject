import pygame as pg
import random
from settings import *
from sprites import *
from os import path

img_dir = path.join(path.dirname(__file__), 'img')

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE),'w') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
    def new(self):
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.run()


    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()
        hits = pg.sprite.spritecollide(self.player,self.platforms, False)
        if hits:
            self.playing = False
        if self.player.rect.top <=0:
            self.player.pos.y = 50
        if self.player.rect.bottom>=HEIGHT:
            self.player.pos.y = HEIGHT
        for plat in self.platforms:
            if plat.rect.top >= HEIGHT:
                plat.kill()
                self.score += 10
        while len(self.platforms) < 30:
            width = random.randrange(15,40)
            p = Platform(self,random.randrange(0,WIDTH - width),
                         random.randrange(-2*HEIGHT,-40), width, width, ENEMY_VEL)
            self_collision = pg.sprite.spritecollide(p,self.platforms, False)
            if self_collision:
                p.kill()
            self.platforms.add(p)
            self.all_sprites.add(p)
            self.platforms.update()


    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.running = False
                self.playing = False


    def draw(self):
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score),28,WHITE,WIDTH/2,15)
        pg.display.flip()

    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        background = pg.image.load(path.join(img_dir,"bg.jpg")).convert()
        background_rect = background.get_rect()
        self.screen.blit(background,background_rect)
        self.draw_text(TITLE,80,WHITE,WIDTH/2,HEIGHT/4)
        self.draw_text("Press arrows to move and dodge the enemies!!!",30,WHITE,WIDTH/2,HEIGHT/2)
        self.draw_text("Press a key to play",22,WHITE,WIDTH/2,HEIGHT*0.75)
        self.draw_text("Highscore: "+ str(self.highscore),22,WHITE,WIDTH/2,15)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER!!!",48,WHITE,WIDTH/2,HEIGHT/4)
        if self.score <= self.highscore:
            self.draw_text("Sometimes it is better to play with focus",26,RED,WIDTH/2,HEIGHT*0.4)
            self.draw_text("YOUR SCORE: " + str(self.score),22,WHITE,WIDTH/2,HEIGHT/2)
            self.draw_text("Highscore: "+ str(self.highscore),22,GREEN,WIDTH/2,HEIGHT*0.6)
            self.draw_text("NOW GO AND BEAT THE HIGH SCORE!",22,WHITE,WIDTH/2,HEIGHT*0.7)
        self.draw_text("Press a key to play again",22,YELLOW,WIDTH/2,HEIGHT*0.8)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!",22,BLUE,WIDTH/2,HEIGHT*0.4)
            self.draw_text("Score: " + str(self.highscore),22,WHITE,WIDTH/2,HEIGHT*0.5)
            self.draw_text("Only the hardest stone makes its mark",26,RED,WIDTH/2,HEIGHT*0.6)
            with open(path.join(self.dir,HS_FILE),'w') as f:
                f.write(str(self.score))
        pg.display.flip()
        self.wait_for_key()

    def draw_text(self,text,size,color,x,y):
        font = pg.font.Font(self.font_name,size)
        text_surface = font.render(text,True,color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface,text_rect)
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
