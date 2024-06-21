import pygame as pg
from sprite_sheet import sprite_sheet
from abc import ABC
from random import randint
from math import log2

class Positions(ABC):
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

class Lixo(Positions):

    def __init__(self, pos_x, pos_y, id, frame_count):
        super().__init__(pos_x, pos_y)
        self.id = id
        self.frame_count = frame_count
        self.angle = 0
    
    @property
    def x(self):
        return self.pos_x
    
    @property
    def y(self):
        return self.pos_y
    
    @property
    def sprite_id(self):
        return self.id
    
    @property
    def obj_angle(self):
        return self.angle
    
    def draw(self, screen, img, pos_x_screen):
        screen.blit(img, (self.x-pos_x_screen, self.y))


class Player(Positions):

    def __init__(self, pos_x, pos_y, speed_obj, width, height):
        super().__init__(pos_x, pos_y)
        self.speed_obj = speed_obj
        self.width = width
        self.height = height
        self.default_tuple = (pos_x, pos_y, speed_obj, width, 3)
        self.space = False
        self.capturando = False
        self.descendo = True
        self.y_base = pos_y
        self.saindo = False
        self.contador = 0

    @property
    def x(self):
        return self.pos_x
    
    @property
    def y(self):
        return self.pos_y
    
    @property
    def speed(self):
        return self.speed_obj

    @property
    def player_width(self):
        return self.width

    def capturar(self, height):
        if self.capturando:
            self.pos_y += self.speed
            if self.pos_y >= 0.8*height:
                self.pos_y = 0.8*height
                self.capturando = False
        else:
            self.pos_y -= self.speed
            if self.pos_y <= self.y_base:
                self.pos_y = self.y_base
                self.space = False
    
    def entregar(self, y_screen):
        if self.capturando:
            self.pos_y += self.speed
            if self.pos_y >= 0.8*y_screen - self.height:
                self.pos_y = 0.8*y_screen - self.height
                self.capturando = False
            else:
                if self.contador == 100:
                    pg.mixer.init()
                    pg.mixer.music.load("audio/Assar_carne.mp3")
                    pg.mixer.music.play()
                    
                self.contador += 1
                
    
    def mexer(self):
        if self.descendo:
            self.pos_y += self.speed//5
            if self.pos_y >= self.y_base+15:
                self.descendo = False
        else:
            self.pos_y -= self.speed//5
            if self.pos_y <= self.y_base-15:
                self.descendo = True
        
    
    def move(self, direcao, height, width, pos_x_screen, y_screen, counter):
        if not self.saindo:
            if not self.space:
                if direcao[pg.K_d] and self.x < pg.display.get_window_size()[0] - self.player_width:
                    self.pos_x += self.speed
                    if self.pos_x > pg.display.get_window_size()[0] - self.player_width:
                        self.pos_x = pg.display.get_window_size()[0] - self.player_width
                if direcao[pg.K_a] and self.x > 0:
                    self.pos_x -= self.speed
                    if self.pos_x < 0:
                        self.pos_x = 0
                if direcao[pg.K_SPACE] and self.x > 0:
                    self.space = True
                    self.capturando = True
                if direcao[pg.K_i] and (counter.lipidio > 0 or counter.proteina > 0):
                    self.saindo = True
                self.mexer()
            else:
                self.capturar(height)
                
            return False, self.saindo, pos_x_screen
        else:
            if self.pos_x < int(width*1.5) - pos_x_screen - self.width//2 or pos_x_screen < width:
                self.pos_x += self.speed//2
                if self.pos_x > int(width*1.5) - pos_x_screen - self.width//2:
                    self.pos_x = int(width*1.5) - pos_x_screen - self.width//2
                pos_x_screen += self.speed//2
                if pos_x_screen > width:
                    pos_x_screen = width
                self.mexer()
            else:
                if not self.capturando:
                    self.contador += 1
                if self.contador == 100:
                    self.space = True
                    self.capturando = True
                if self.contador == 700:
                    return True, self.saindo, pos_x_screen
                elif self.contador >= 100:
                    self.entregar(y_screen)
            
            return False, self.saindo, pos_x_screen
                
    
    def animate(self, animation_i, screen):
        if not self.capturando and not self.space and not self.saindo:
            screen.blit(sprite_sheet[4][0], (self.x, self.y))
        elif self.capturando and self.space and not self.saindo:
            screen.blit(sprite_sheet[4][1], (self.x, self.y))
        else:
            screen.blit(sprite_sheet[4][2], (self.x, self.y))
        return animation_i
        
    def game_over(self):
        return False

    def restart(self):
        self.pos_x = self.default_tuple[0]
        self.pos_y = self.default_tuple[1]
        self.speed_obj = self.default_tuple[2]
        self.width = self.default_tuple[3]
        self.lives = self.default_tuple[4]
