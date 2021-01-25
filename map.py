import pygame
from mazegen import generate
from gen_map import way

while True:
    
    tx_map = generate(17, 7)
    if way(tx_map, 2, 2, 16, 6):
        break


worlds = set()
info_colis = []
for i, j in enumerate(tx_map):
    for k, n in enumerate(j):
        if n == '1':
            worlds.add((k * 100, i * 100))
            info_colis.append(pygame.Rect(k * 100, i * 100, 100, 100))
