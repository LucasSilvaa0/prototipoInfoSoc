import pygame as pg
from random import randint
from objects import Lixo
from button import Button_Play_Again
from sprite_sheet import sprite_sheet
from math import log2

def spawn_lixo(frame_count):

    width, height = pg.display.get_window_size()

    randint_x = randint(width//6,int(5*width//6))
    randint_y = 0.8*height

    obj = Lixo(randint_x, randint_y, randint(0, 2), frame_count)

    # pra não ficar um módulo circular, é melhor dar blit(return[0], return[1])

    return [sprite_sheet[obj.sprite_id], obj]

def game_diff(frame_count, dificuldade, onscreen):

    speed_game = int(log2(4 + int(frame_count/300)))

    dificuldade = int(log2(1 + int(frame_count/360)))+1

    if frame_count % int(100/(dificuldade/1.5)) == 0 and len(onscreen) < 1 + dificuldade * 1.1:
        lixo_novo = spawn_lixo(frame_count)
        onscreen.append(lixo_novo)

    # Aumentar o spawnrate a cada segundo
    
    return frame_count, dificuldade, onscreen, speed_game
    
def remove_obj(removidos, item, screen, pos_x_screen):
  if item[1].y > screen.get_height() or item[1].x + 100 - pos_x_screen <= 0:
    removidos.append(item)
  return removidos

def init_game():
    pg.display.init()
    x_screen, y_screen = pg.display.Info().current_w, pg.display.Info().current_h
    screen = pg.display.set_mode((int(x_screen/2), int(3*y_screen/4)))
    pg.display.set_caption('MangueBit')
    x_screen, y_screen = screen.get_size()

    clock = pg.time.Clock()
    
    frame_count = 0

    onscreen = []
    dificuldade = 1
    running = True
    angle = 0
    crab_animation = 0
    return 0, x_screen, y_screen, screen, clock, frame_count, onscreen, dificuldade, running, angle, crab_animation

def init_sprites(screen, sprites_player):

  background_game = pg.image.load('graphics/OIG3.png')
  background_game = pg.transform.scale(background_game, (screen.get_width()*2, screen.get_height()))
  background_finished = pg.image.load('graphics/carne.webp')

  counter_box = pg.image.load('graphics/counter_background.png')

  play_again = Button_Play_Again('graphics/Button_play_again.png', screen)

  crab = sprites_player
  pg.display.set_icon(crab[-1])

  return background_game, counter_box, crab, background_finished, play_again


def dark_screen(surface, wid, height, alpha=150):
    overlay = pg.Surface((wid, height), pg.SRCALPHA)
    overlay.fill((0, 0, 0, alpha))
    surface.blit(overlay, (0, 0))

def draw_finish(screen, background_finished, x_screen, y_screen):
  pg.font.init()
  font_carne = pg.font.Font(None, 57)
  color_font = (255,255,255)
  
  screen.blit(background_finished, (x_screen//2 - background_finished.get_width()//2, y_screen//2 - background_finished.get_height()//2))
  
  text_carne_record = font_carne.render(f'Carne pronta!', True, color_font)
  screen.blit(text_carne_record, (x_screen//2 + 32, y_screen//2 + 134))
