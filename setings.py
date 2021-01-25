import math

width = 1200
height = 800
half_width = width // 2
half_height = height // 2

fov = math.pi / 3
half_fov = fov / 2
num_rays = 120
max_depth = 800
delta_angle = fov / num_rays
dist = num_rays / (2 * math.tan((half_fov)))
proj_co = 3 * dist * 100
scale = width // num_rays

tx_width = 1200
tx_hight = 1200
tx_scale = tx_width // 100

# player_pos = (half_width, half_height)
player_pos = (100, 100)
player_angle = 0
player_speed = 2

fps = 60