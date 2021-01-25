import pygame
from mazegen import generate
from gen_map import way

'''while True:
    
    tx_map = generate(17, 7)
    print('all')
    if way(tx_map, 1, 1, 16, 6):
        break'''

tx_map = generate(17, 7)
#print(tx_map[5][15])
print(way(tx_map, 2, 2, 16, 6))