import pygame
from mazegen import generate

'''tx_map = [
    '1111111111111111',
    '1000000000111001',
    '1000000000000001',
    '1000011111000001',
    '1000000000000001',
    '1111100000000001',
    '1111100000000001',
    '1111111111111111',
]'''
tx_map = generate(17, 7)

worlds = set()
info_colis = []
for i, j in enumerate(tx_map):
    for k, n in enumerate(j):
        if n == '1':
            worlds.add((k * 100, i * 100))
            info_colis.append(pygame.Rect(k * 100, i * 100, 100, 100))
