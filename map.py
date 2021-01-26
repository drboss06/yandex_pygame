import pygame

tx_map = [
    '1111111111111111',
    '1000000000111001',
    '1000000000000001',
    '1000011111000001',
    '1000000000000001',
    '1111100000000001',
    '1011100000000001',
    '1111111111111111',
]

worlds = set()
info_colis = []
mapGrid =[]
mapBoundX, mapBoundY = len(tx_map[0]), len(tx_map)
for i, j in enumerate(tx_map):
    mapGrid.append(list(map(int, j)))
    for k, n in enumerate(j):
        if n == '1':
            worlds.add((k * 100, i * 100))
            info_colis.append(pygame.Rect(k * 100, i * 100, 100, 100))
