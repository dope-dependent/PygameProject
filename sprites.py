import pygame as pg
from settings import *
from os import path
vec = pg.math.Vector2


img_dir = path.join(path.dirname(__file__), 'img')



class Player(pg.sprite.Sprite):
    def __init__(self,game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        player_img = pg.image.load(path.join(img_dir,"rocket.png")).convert()
        player_img = pg.transform.scale(player_img, (40,52))
        player_rect = player_img.get_rect()
        self.image = player_img
        self.rect = player_rect
        self.rect.center = (WIDTH/2 , HEIGHT/2 )
        self.pos = vec(WIDTH/2 , HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
    def update(self):
        self.acc = vec(0,0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_UP]:
            self.acc.y = -PLAYER_ACC
        if keys[pg.K_DOWN]:
            self.acc.y = PLAYER_ACC
        #Game kinematics control
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.acc.y += self.vel.y * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5*self.acc
        #wrap around the sides
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        self.rect.midbottom = self.pos

class Platform(pg.sprite.Sprite):
    def __init__(self,game,x,y,w,h,v):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.score = game.score
        rock_img = pg.image.load(path.join(img_dir,"rock.png")).convert()
        rock_img = pg.transform.scale(rock_img, (h,w))
        rock_rect = rock_img.get_rect()
        self.image = rock_img
        self.rect = rock_rect
        self.rect.x = x
        self.rect.y = y
        self.pos = vec(x,y)
        self.vel = vec(0,v)

    def update(self):
        self.rect.top += self.vel.y
        self.vel.y = ENEMY_VEL + self.score*0.001
