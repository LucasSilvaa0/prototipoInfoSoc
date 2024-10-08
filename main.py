import pygame as pg
from functions import game_diff, remove_obj, init_game, init_sprites, dark_screen, draw_finish
from objects import Player
from sprite_sheet import sprites_player
from time import sleep
from counters import Points_Counter

pg.display.init()
pg.font.init()

pos_x_screen, x_screen, y_screen, screen, clock, frame_count, onscreen, dificuldade, running, angle, animation_i = init_game()

background_game, counter_box, crab, background_finished, play_again = init_sprites(screen, sprites_player)

sprites_bioimpressora = pg.image.load('graphics/impressora.png')

font_carne = pg.font.Font(None, 57)
color_font = (255,255,255)


reiniciar = 0

while True:

    clock = pg.time.Clock()
    drone_player = Player(x_screen/2-int(crab[0].get_width())//2, int(y_screen*0.2125), 7, int(crab[0].get_width()), int(crab[0].get_height()))


    my_font = pg.font.SysFont('arial', 36)

    counter = Points_Counter()
    esc = False
        
    while running:
            screen.blit(background_game, (0-pos_x_screen, 0))
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    running = False
                    exit()
            
            
            keys = pg.key.get_pressed()
            
            if not esc:
                if reiniciar:
                    reiniciar = False
                    pos_x_screen = 0
                    screen.blit(background_game, (0-pos_x_screen, 0))
                frame_count, dificuldade, onscreen, speed_game = game_diff(frame_count, dificuldade, onscreen)
                animation_i = drone_player.animate(animation_i, screen)
                esc, acabando, pos_x_screen = drone_player.move(keys, y_screen, x_screen, pos_x_screen, y_screen, counter)

                removidos = []
                colididos = []
                for item in onscreen:
                    removidos = remove_obj(removidos, item, screen, pos_x_screen)
                    colididos = counter.collide(colididos, drone_player, crab, item)
                    item[1].draw(screen, pg.transform.rotate(item[0], item[1].obj_angle), pos_x_screen)

                counter.draw_counter(screen, counter_box)
                screen.blit(sprites_bioimpressora, (1.5*x_screen-pos_x_screen-sprites_bioimpressora.get_width()//2, y_screen*0.65))
                
                text_carne_record = font_carne.render(f'BIOIMPRESSORA 3D!', True, color_font)
                screen.blit(text_carne_record, (1.5*x_screen-pos_x_screen-text_carne_record.get_width()//2, y_screen*0.7 + sprites_bioimpressora.get_height()))
                
                for i in removidos:
                    onscreen.remove(i)
                for i in colididos:
                    onscreen.remove(i)
            else:
                screen.blit(background_game, (0-pos_x_screen,0))
                animation_i = drone_player.animate(animation_i, screen)
                dark_screen(screen, x_screen, y_screen)
                draw_finish(screen, background_finished, x_screen, y_screen)
                play_again.draw_button()

                if play_again.update():
                    reiniciar = True
                    
                    sleep(1)

                    esc = False

                    drone_player.restart()
                    onscreen = []
                    
                    frame_count = -1
                    counter = Points_Counter()

            pg.display.update()

            frame_count += 1

            clock.tick(60)
            if reiniciar:
                break
    
    if reiniciar:
        continue