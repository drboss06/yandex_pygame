import pygame
import setings as st
import math
from map import worlds, info_colis
import pygame.gfxdraw
# my_branch
pygame.init()
disp = pygame.display.set_mode((st.width, st.height))
clock = pygame.time.Clock()
running = True

class Draw:
    def __init__(self):
        self.well = pygame.image.load('img1.png').convert()

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
                si = 0.00001

            if not co:
                co = 0.00001
            k += 1
            for j in range(st.max_depth):
                x = xo + j * co
                y = yo + j * si
                de_v = (x - xo) / co
                de_h = (y - yo) / si
                yv = yo + de_v * si
                xh = xo + de_h * co
                if (x // 100 * 100, y // 100 * 100) in worlds:
                    j *= math.cos(player_angle - cur_a)
                    if j != 0:
                        pro = int(st.proj_co / j)
                        col = 255 / (1 + j * j * 0.00002)
                        try:
                            if de_h < de_v:
                                ofset = yv
                            else:
                                ofset = xh
                            ofset = int(ofset) % 100
                            well_col = self.well.subsurface(ofset * st.tx_scale, 0, st.tx_scale, st.tx_hight)
                        except:
                            k = 0
                            if de_h < de_v:
                                ofset = yv
                            else:
                                ofset = xh
                            ofset = int(ofset) % 100
                            well_col = self.well.subsurface(ofset * st.tx_scale, 0, st.tx_scale, st.tx_hight)
                        well_col = pygame.transform.scale(well_col, (st.scale, pro))
                        disp.blit(well_col, (i * st.scale, st.half_height - pro // 2))
                        pygame.gfxdraw.box(disp, pygame.Rect(i * st.scale, st.half_height - pro // 2, st.scale, pro), (0, 0, 0, 255 - col))
                        break
            cur_a += st.delta_angle


class Player:
    def __init__(self):
        self.x, self.y = st.player_pos
        self.angle = st.player_angle
        self.rect = pygame.Rect(self.x, self.y, 24, 24)

    def colis(self, dx, dy):
        self.rect.update(self.x + dx, self.y + dy, 24, 24)
        for i in info_colis:
            if self.rect.colliderect(i):
                return False
        return True


    @property
    def pos(self):
        return  (self.x, self.y)


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
    player.movement()
    disp.fill(pygame.Color('black'))

    pygame.draw.rect(disp, (0, 186, 255), (0, 0, st.width, st.half_width))
    pygame.draw.rect(disp, (40, 40, 40), (0, st.half_height, st.width, st.half_width))
    draw.ray_cast(player, disp, player.pos, player.angle)
    pygame.draw.rect(disp, pygame.Color('red'), (int(player.x), int(player.y), 24, 24))
    pygame.draw.line(disp, pygame.Color('red'), player.pos, (player.x + st.width * math.cos(player.angle),
                                                             player.y + st.width * math.sin(player.angle)))
    for x, y in worlds:
        pygame.draw.rect(disp, (0, 255, 0), (x, y, 100, 100), 2)

    pygame.display.flip()
    clock.tick(st.fps)
