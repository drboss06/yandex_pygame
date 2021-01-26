import math

import pygame
import pygame.gfxdraw

import setings as st
from map import info_colis, worlds

pygame.init()
disp = pygame.display.set_mode((st.width, st.height))
clock = pygame.time.Clock()
running = True
texture = pygame.image.load('img4.bmp')
texWidth = texture.get_width()
texHeight = texture.get_height()
texArray = pygame.PixelArray(texture)


class Draw:
    def __init__(self):
        
        self.magicvar = 1
        self.well = pygame.image.load('img1.png').convert()
        self.texArray = pygame.PixelArray(self.well)
        self.dirX, self.dirY = 1.0, 0.0
        self.planeX, self.planeY = 0.0, 0.66
    
    def ray_cast(self, player, disp, player_pos, player_angle):
        si = math.sin(st.player_angle)
        co = math.cos(st.player_angle)
        cur_a = player_angle - st.half_fov
        xo, yo = player_pos
        k = 0
        for i in range(st.num_rays):
            si = math.sin(cur_a)
            co = math.cos(cur_a)
            if not si:
                si = 1 * 10 ** -15
            
            if not co:
                co = 1 * 10 ** -15
            k += 1
            for j in range(st.max_depth):
                varx = xo + j * co
                vary = yo + j * si
                de_v = (varx - xo) / co
                de_h = (vary - yo) / si
                yv = yo + de_v * si
                xh = xo + de_h * co
                # print((varx // 100 * 100, vary // 100 * 100),(math.ceil(varx) - varx%100, math.ceil(vary)-vary%100))
                if (varx // 100 * 100, vary // 100 * 100) in worlds:
                    # if (math.floor(varx) - math.floor(varx)%100, math.floor(vary)-math.floor(varx)%100) in worlds:
                    j *= math.cos(player_angle - cur_a)
                    if j != 0:
                        pro = int(st.proj_co / j)
                        drawStart = pro
                        drawEnd = pro
                        col = 255 / (1 + j * j * 0.00002)
                        if de_h <= de_v:
                            ofset = yv
                        else:
                            ofset = xh
                        ofset = int(ofset) % 100 * self.magicvar
                        well_col = self.well.subsurface(ofset * st.tx_scale, 0, st.tx_scale,
                                                        st.tx_hight)
                        # well_col = self.well.subsurface(ofset, 0, 1, 100)t)
                        well_col = pygame.transform.scale(well_col, (st.tx_scale, pro))
                        disp.blit(well_col, (i * st.scale, st.half_height - pro // 2))
                        # for yuy in range(texHeight):
                        #     # Ignore pixels that are off of the screen
                        #     if drawStart + ((st.half_height - pro // 2) / st.tx_hight) * (yuy + 1) < 0:
                        #         continue
                        #     if drawStart + ((st.half_height - pro // 2) / st.tx_hight) * yuy > st.height:
                        #         break
                        #
                        #     # Load pixel's colour from array
                        #
                        #     # colour = pygame.Color(self.texArray[yv][yuy])
                        #
                        #     colour = (255, 255, 255, 255)
                        #     # Darkens environment with distance
                        #     c = 255.0 - abs(int(j * 32)) * 0.85
                        #     if c < 1:
                        #         c = 1
                        #     if c > 255:
                        #         c = 255
                        #
                        #     # Different faces have different luminence to add to the 3D effectd
                        #
                        #     # Change the luminence if necessary
                        #     new_colour = []
                        #     for i, value in enumerate(colour):
                        #         if i == 0:
                        #             continue  # Exclude the alpha value
                        #         new_colour.append(value * (c / 255))
                        #     colour = tuple(new_colour)
                        #     # print(colour)
                        #     pygame.draw.line(disp, colour, (xo, drawStart + ((st.half_height - pro // 2) / st.tx_hight) * yuy),
                        #                      (xo, drawStart + ((st.half_height - pro // 2) / st.tx_hight) * (yuy + 1)), st.num_rays)
                        #
                        # disp.blit(well_col, (i * st.scale, st.half_height - pro // 2))
                        pygame.gfxdraw.box(disp, pygame.Rect(i * st.scale, st.half_height - pro // 2,
                                                             st.scale, pro),
                                           (0, 0, 0, 255 - int(col)))
                        break
            cur_a += st.delta_angle
        
        # for x in range(0, st.width, st.num_rays):
        #     # Initial setup
        #     cameraX = 2 * x / st.width - 1
        #     rayPosX = player_pos[0]
        #     rayPosY = player_pos[1]
        #     rayDirX = self.dirX + self.planeX * cameraX + 0.000000000000001  # Add small value to avoid division by 0
        #     rayDirY = self.dirY + self.planeY * cameraX + 0.000000000000001  # Add small value to avoid division by 0
        #
        #     # Which square on the map the ray is in
        #     mapX = int(rayPosX)
        #     mapY = int(rayPosY)
        #
        #     # The length of one ray from one x-side or y-side to the next x-side or y-side
        #     deltaDistX = math.sqrt(1 + rayDirY ** 2 / rayDirX ** 2)
        #     deltaDistY = math.sqrt(1 + rayDirX ** 2 / rayDirY ** 2)
        #     zBuffer = []
        #
        #     # Calculate step and initial sideDist
        #     if rayDirX < 0:
        #         stepX = -1
        #         sideDistX = (rayPosX - mapX) * deltaDistX
        #     else:
        #         stepX = 1
        #         sideDistX = (mapX + 1 - rayPosX) * deltaDistX
        #
        #     if rayDirY < 0:
        #         stepY = -1
        #         sideDistY = (rayPosY - mapY) * deltaDistY
        #     else:
        #         stepY = 1
        #         sideDistY = (mapY + 1 - rayPosY) * deltaDistY
        #
        #     # Digital differential analysis (DDA)
        #     while True:
        #         # Jump to next map square
        #         if sideDistX < sideDistY:
        #             sideDistX += deltaDistX
        #             mapX += stepX
        #             side = 0
        #         else:
        #             sideDistY += deltaDistY
        #             mapY += stepY
        #             side = 1
        #
        #         # Check if ray hits wall or leaves the map boundries
        #         if mapX >= self.mapBoundX or mapY >= self.mapBoundY or mapX < 0 or mapY < 0 or self.mpGrid[mapX][
        #             mapY] > 0:
        #             break
        #
        #     # Calculate the total length of the ray
        #     if side == 0:
        #         rayLength = (mapX - rayPosX + (1 - stepX) / 2) / rayDirX
        #     else:
        #         rayLength = (mapY - rayPosY + (1 - stepY) / 2) / rayDirY - 0.000000000001
        #
        #     # Calculate the length of the line to draw on the screen
        #     lineHeight = (st.height / rayLength) * st.tx_hight
        #
        #     # Calculate the start and end point of each line
        #     drawStart = -lineHeight / 2 + (st.height) / 2
        #     drawEnd = lineHeight / 2 + (st.height) / 2
        #
        #     # Calculate where exactly the wall was hit
        #     if side == 0:
        #         wallX = rayPosY + rayLength * rayDirY
        #     else:
        #         wallX = rayPosX + rayLength * rayDirX
        #     wallX = abs((wallX - math.floor(wallX)) - 1)
        #
        #     # Find the x coordinate on the texture
        #     texX = int(wallX * st.tx_width)
        #     if side == 0 and rayDirX > 0:
        #         texX = st.tx_width - texX - 1
        #     if side == 1 and rayDirY < 0:
        #         texX = st.tx_width - texX - 1
        #
        #     for y in range(st.tx_hight):
        #         # Ignore pixels that are off of the screen
        #         if drawStart + (lineHeight / st.tx_hight) * (y + 1) < 0:
        #             continue
        #         if drawStart + (lineHeight / st.tx_hight) * y > st.height:
        #             break
        #
        #         # Load pixel's colour from array
        #         colour = pygame.Color(self.texArray[texX][y])
        #
        #         # Darkens environment with distance
        #         c = 255.0 - abs(int(rayLength * 32)) * 0.85
        #         if c < 1:
        #             c = 1
        #         if c > 255:
        #             c = 255
        #
        #         # Different faces have different luminence to add to the 3D effect
        #         if side == 1:
        #             c *= 0.75
        #
        #         # Change the luminence if necessary
        #         new_colour = []
        #         for i, value in enumerate(colour):
        #             if i == 0:
        #                 continue  # Exclude the alpha value
        #             new_colour.append(value * (c / 255))
        #         colour = tuple(new_colour)
        #
        #         pygame.draw.line(disp, colour, (x, drawStart + (lineHeight / st.tx_hight) * y),
        #                          (x, drawStart + (lineHeight / st.tx_hight) * (y + 1)), st.num_rays)


class Player:
    def __init__(self):
        self.x, self.y = st.player_pos
        self.angle = st.player_angle
        self.rect = pygame.Rect(self.x - 12, self.y - 12, 24, 24)
    
    def colis(self, dx, dy):
        self.rect.update(self.x + dx - 12, self.y + dy - 12, 24, 24)
        for i in info_colis:
            if self.rect.colliderect(i):
                return False
        return True
    
    @property
    def pos(self):
        return (self.x, self.y)
    
    def movement(self):
        si = math.sin(self.angle)
        co = math.cos(self.angle)
        pygame.mouse.set_visible(False)
        pres = pygame.key.get_pressed()
        difference = pygame.mouse.get_pos()[0] - (st.width / 2)
        pygame.mouse.set_pos([st.width / 2, st.height / 2])
        
        if difference:
            self.angle += difference / 100
        if pres[pygame.K_w]:
            dy = st.player_speed * si
            dx = st.player_speed * co
            if self.colis(dx, dy):
                self.x += dx
                self.y += dy
        if pres[pygame.K_s]:
            dy = -st.player_speed * si
            dx = -st.player_speed * co
            if self.colis(dx, dy):
                self.x += dx
                self.y += dy
        if pres[pygame.K_d]:
            dy = st.player_speed * co
            dx = -st.player_speed * si
            if self.colis(dx, dy):
                self.x += dx
                self.y += dy
        if pres[pygame.K_a]:
            dy = -st.player_speed * co
            dx = st.player_speed * si
            if self.colis(dx, dy):
                self.x += dx
                self.y += dy
        if pres[pygame.K_LEFT]:
            self.angle -= 0.06
        if pres[pygame.K_RIGHT]:
            self.angle += 0.06


player = Player()
draw = Draw()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_q:
                draw.magicvar = round(0.1 + draw.magicvar, 2)
            print(draw.magicvar)
            if event.key == pygame.K_e:
                draw.magicvar = round(-0.1 + draw.magicvar, 2)
            print(draw.magicvar)
    player.movement()
    disp.fill(pygame.Color('black'))
    
    pygame.draw.rect(disp, (0, 186, 255), (0, 0, st.width, st.half_width))
    pygame.draw.rect(disp, (40, 40, 40), (0, st.half_height, st.width, st.half_width))
    draw.ray_cast(player, disp, player.pos, player.angle)
    pygame.draw.rect(disp, pygame.Color('red'), (int(player.x) - 12, int(player.y) - 12, 24, 24))
    pygame.draw.line(disp, pygame.Color('red'), player.pos,
                     (player.x + st.width * math.cos(player.angle),
                      player.y + st.width * math.sin(player.angle)))
    for x, y in worlds:
        pygame.draw.rect(disp, (0, 255, 0), (x, y, 100, 100), 2)
    
    pygame.display.flip()
    clock.tick(st.fps)
