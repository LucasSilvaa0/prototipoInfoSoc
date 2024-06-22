import pygame as pg

sprites_pitu = pg.image.load('graphics/lixo_resized.webp')
sprites_bottle = pg.image.load('graphics/lipidio.png')
sprites_tire = pg.image.load('graphics/proteina.png')

sprites_mangues = [pg.image.load('graphics/swamp.png')]

sprites_player = [pg.image.load('graphics/drone_voando_resized.webp'), pg.image.load('graphics/drone_capturando_resized.webp'), pg.image.load('graphics/drone_voltando_resized.webp')]

sprite_sheet = [sprites_pitu, sprites_bottle, sprites_tire, sprites_mangues, sprites_player]
