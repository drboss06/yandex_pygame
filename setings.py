import math


TILE = 100

width = 1200
height = 800
half_width = width // 2
half_height = height // 2

fov = math.pi / 3
half_fov = fov / 2
num_rays = 300
max_depth = 800
delta_angle = fov / num_rays
dist = num_rays / (2 * math.tan(half_fov))
proj_co = 3 * dist * TILE
scale = width // num_rays

DOUBLE_PI = math.tau
CENTER_RAY = num_rays//2 - 1
FAKE_RAYS = 100

tx_width = 1200
tx_hight = 1200
tx_scale = tx_width // TILE

fps = 60

# Maze
maze_length = 33
maze_width = 33

player_pos = (112, 112)
player_angle = 0
player_speed = 8
