import pygame
from mazegen import generate
from gen_map import way
from setings import maze_length, maze_width, TILE

tx_map = generate(maze_length, maze_width)
tx_map[-2] = tx_map[-2][:-2] + "21"

worlds = {}
info_colis = []
for i, j in enumerate(tx_map):
    for k, n in enumerate(j):
        if n == '1':
            worlds[(k * TILE, i * TILE)] = '1'
            info_colis.append(pygame.Rect(k * 100, i * 100, 100, 100))
        if n == '2':
            worlds[(k * TILE, i * TILE)] = '2'
        if n == '3':
            worlds[(k * TILE, i * TILE)] = '3'
            info_colis.append(pygame.Rect(k * 100, i * 100, 100, 100))
