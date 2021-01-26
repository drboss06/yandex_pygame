import math
import pygame
import pygame.gfxdraw
import setings as st
from map import info_colis, worlds
from random import randint

pygame.init()
disp = pygame.display.set_mode((st.width, st.height))
clock = pygame.time.Clock()
running = True
tab = False

class Draw:
    def __init__(self):
        
        self.magicvar = 1
        self.well = pygame.image.load('img1.png').convert()
        self.texArray = pygame.PixelArray(self.well)
        self.dirX, self.dirY = 1.0, 0.0
        self.planeX, self.planeY = 0.0, 0.66
        self.mat = randint(1, 20)

    def start_screen(self):
        intro_text = ['СПАСИБО ЗА 100 БАЛЛОВ','',
                        'Делали эту хуйню' if self.mat < 3 else 'Делали эту фигню',
                        'Zeldini, sadfun, ArtiArtem']


        fon = pygame.transform.scale(pygame.image.load('fon.png'), (st.width, st.height))
        disp.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            disp.blit(string_rendered, intro_rect)
    
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
                if (varx // 100 * 100, vary // 100 * 100) in worlds:
                    j *= math.cos(player_angle - cur_a)
                    if j != 0:
                        pro = int(st.proj_co / j)
                        col = 255 / (1 + j * j * 0.00002)
                        if de_h <= de_v:
                            ofset = yv
                        else:
                            ofset = xh
                        ofset = int(ofset) % 100 * self.magicvar
                        well_col = self.well.subsurface(ofset * st.tx_scale, 0, st.tx_scale,
                                                        st.tx_hight)
                        well_col = pygame.transform.scale(well_col, (st.tx_scale, pro))
                        
                        disp.blit(well_col, (i * st.scale, st.half_height - pro // 2))
                        pygame.gfxdraw.box(disp, pygame.Rect(i * st.scale, st.half_height - pro // 2,
                                                             st.scale + 2, pro),
                                           (0, 0, 0, 255 - int(col)))
                        break
            cur_a += st.delta_angle


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
        xf, yf = player.pos
        if xf // 100 == st.maze_length - 2 and yf // 100 == st.maze_width - 2:
            running = False
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
            if event.key == pygame.K_TAB:
                tab = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                tab = True

    player.movement()
    disp.fill(pygame.Color('black'))
    
    pygame.draw.rect(disp, (0, 186, 255), (0, 0, st.width, st.half_width))
    pygame.draw.rect(disp, (40, 40, 40), (0, st.half_height, st.width, st.half_width))
    draw.ray_cast(player, disp, player.pos, player.angle)

    if tab:
        pygame.draw.rect(disp, pygame.Color('red'), (int(player.x) // 10, int(player.y) // 10, 5, 5))
        for x, y in worlds:
            if x // 100 == st.maze_length - 1 and y // 100 == st.maze_width - 1:
                pygame.draw.rect(disp, (255, 0, 0), (x // 10, y // 10, 10, 10))
            else:
                pygame.draw.rect(disp, (0, 255, 0), (x // 10, y // 10, 10, 10), 2)
    
    pygame.display.flip()
    clock.tick(st.fps)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_q:
                draw.magicvar = round(0.1 + draw.magicvar, 2)
            if event.key == pygame.K_e:
                draw.magicvar = round(-0.1 + draw.magicvar, 2)


    disp.fill(pygame.Color('black'))

    draw.start_screen()
    pygame.display.flip()
    clock.tick(st.fps)
