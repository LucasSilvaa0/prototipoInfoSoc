import pygame as pg
from time import time

class Stopwatch:
    
    def __init__(self, start_time):
        self._start_time = start_time
        
    def draw_stopwatch(self, screen, my_font, x_screen, image_background):
        screen.blit(image_background, (x_screen*(9/10) - 80, 15))
        screen.blit(my_font.render(f'{time() - self._start_time:.2f}', False, (255,255,255)), (x_screen*(9/10) - 40, 20))


class Points_Counter:
    
    def __init__(self):
        self.lixo = 0
        self.lipidio = 0
        self.proteina = 0
    
    def collide(self, colididos, crab_player, crab, item):
        item_rec = item[0].get_rect(topleft=(item[1].x, item[1].y))
        crab_rec = crab[0].get_rect(topleft=(crab_player.x, crab_player.y))
        
        if crab_rec.colliderect(item_rec):
            if item[1].sprite_id == 0:
                self.lixo += 1
            elif item[1].sprite_id == 1:
                self.lipidio += 1
            else:
                self.proteina += 1
            
            colididos.append(item)
        
        return colididos
    
    def draw_counter(self, screen, image_background):
        pg.font.init()
        fonte = pg.font.Font(None, 30)
        color_font = (255,255,255)
        
        pitu_counter = fonte.render(f'Lixos: ' + str(self.pitu), True, color_font)
        
        bottle_counter = fonte.render(f'Lipídios: ' + str(self.bottle), True, color_font)
        
        tire_counter = fonte.render(f'Proteínas: ' + str(self.tire), True, color_font)
    
        screen.blit(image_background, (5,10))
        screen.blit(pitu_counter, (25,25))

        screen.blit(image_background, (5,50))
        screen.blit(bottle_counter, (25, 65))

        screen.blit(image_background, (5,90))
        screen.blit(tire_counter, (25, 105))
    
    @property
    def pitu(self):
        return self.lixo
    
    @property
    def bottle(self):
        return self.lipidio
    
    @property
    def tire(self):
        return self.proteina
