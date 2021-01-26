import sys, os, pygame, time
from pygame.locals import *
from math import *

####------Colours------####
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
CYAN = (0, 255, 255)
DARKBLUE = (0, 0, 64)
DARKBROWN = (36, 18, 5)
DARKGREEN = (0, 64, 0)
DARKGREY = (64, 64, 64)
DARKRED = (64, 0, 0)
GREY = (128, 128, 128)
GREEN = (0, 128, 0)
LIME = (0, 255, 0)
MAGENTA = (255, 0, 255)
MAROON = (128, 0, 0)
NAVYBLUE = (0, 0, 128)
OLIVE = (128, 128, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
SILVER = (192, 192, 192)
TEAL = (0, 128, 128)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
####-------------------####

pygame.init()

path = ''

WIDTH = 1360
HEIGHT = 768
map_size = int((WIDTH / 680) * 64)

CLOCK = pygame.time.Clock()
FPS = 120
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)

pygame.display.set_caption("Raycaster")
pygame.mouse.set_visible(False)

map_colour = MAROON
floor_colour = DARKBROWN
ceiling_colour = DARKRED

rotate_speed = 0.01
move_speed = 0.05
strafe_speed = 0.04
wall_height = 1.27
resolution = 6  # Pixels per line

texture = pygame.image.load(os.path.join(path, 'img4.bmp'))
texWidth = texture.get_width()
texHeight = texture.get_height()
texArray = pygame.PixelArray(texture)

HUD = pygame.image.load(os.path.join(path, 'img2.png'))
HUD = pygame.transform.scale(HUD, (
int(HUD.get_width() * (map_size / 64)), int(HUD.get_height() * (map_size / 64))))

old = 0


def create_level(file):
    if file[-4:] != '.txt':
        file += '.txt'
    f = open(os.path.join(path, file), 'r')
    file = f.readlines()
    
    for i, line in enumerate(file):
        file[i] = list(line.rstrip('\n'))
        for j, char in enumerate(file[i]):
            if char == ' ':
                file[i][j] = 0
            else:
                file[i][j] = int(char)
    f.close()
    
    mapBoundX = len(file)
    mapBoundY = len(file[0])
    mapGrid = []
    
    for i, line in enumerate(file):
        mapGrid.append([])
        for j, char in enumerate(file[i]):
            if char != 0:
                mapGrid[i].append(char)
            else:
                mapGrid[i].append(0)
    print(mapBoundX, mapBoundY, mapGrid)
    return mapBoundX, mapBoundY, mapGrid


def Quit():
    pygame.quit()
    sys.exit()


def main():
    mapBoundX, mapBoundY, mapGrid = create_level('Level')
    
    posX, posY = 8.5, 10.5
    dirX, dirY = 1.0, 0.0
    planeX, planeY = 0.0, 0.66
    
    while True:
        
        # Input handling
        for event in pygame.event.get():
            if event.type == QUIT:
                Quit()
                return
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    Quit()
                    return
        
        
        # CEILING AND FLOOR
        pygame.draw.rect(SCREEN, (0, 186, 255), (0, 0, WIDTH, (HEIGHT) / 2))
        pygame.draw.rect(SCREEN, (40, 40, 40),
                         (0, (HEIGHT) / 2, WIDTH, (HEIGHT) / 2))
        
        for x in range(0, WIDTH, resolution):
            # Initial setup
            cameraX = 2 * x / WIDTH - 1
            rayPosX = posX
            rayPosY = posY
            rayDirX = dirX + planeX * cameraX + 0.000000000000001  # Add small value to avoid division by 0
            rayDirY = dirY + planeY * cameraX + 0.000000000000001  # Add small value to avoid division by 0

            # Which square on the map the ray is in
            mapX = int(rayPosX)
            mapY = int(rayPosY)

            # The length of one ray from one x-side or y-side to the next x-side or y-side
            deltaDistX = sqrt(1 + rayDirY ** 2 / rayDirX ** 2)
            deltaDistY = sqrt(1 + rayDirX ** 2 / rayDirY ** 2)
            zBuffer = []

            # Calculate step and initial sideDist
            if rayDirX < 0:
                stepX = -1
                sideDistX = (rayPosX - mapX) * deltaDistX
            else:
                stepX = 1
                sideDistX = (mapX + 1 - rayPosX) * deltaDistX
            
            if rayDirY < 0:
                stepY = -1
                sideDistY = (rayPosY - mapY) * deltaDistY
            else:
                stepY = 1
                sideDistY = (mapY + 1 - rayPosY) * deltaDistY

            # Digital differential analysis (DDA)
            while True:
                # Jump to next map square
                if sideDistX < sideDistY:
                    sideDistX += deltaDistX
                    mapX += stepX
                    side = 0
                else:
                    sideDistY += deltaDistY
                    mapY += stepY
                    side = 1

                # Check if ray hits wall or leaves the map boundries
                if mapX >= mapBoundX or mapY >= mapBoundY or mapX < 0 or mapY < 0 or mapGrid[mapX][
                    mapY] > 0:
                    break

            # Calculate the total length of the ray
            if side == 0:
                rayLength = (mapX - rayPosX + (1 - stepX) / 2) / rayDirX
            else:
                rayLength = (mapY - rayPosY + (1 - stepY) / 2) / rayDirY

            # Calculate the length of the line to draw on the screen
            lineHeight = (HEIGHT / rayLength) * wall_height

            # Calculate the start and end point of each line
            drawStart = -lineHeight / 2 + (HEIGHT) / 2
            drawEnd = lineHeight / 2 + (HEIGHT) / 2

            # Calculate where exactly the wall was hit
            if side == 0:
                wallX = rayPosY + rayLength * rayDirY
            else:
                wallX = rayPosX + rayLength * rayDirX
            wallX = abs((wallX - floor(wallX)) - 1)

            # Find the x coordinate on the texture
            texX = int(wallX * texWidth)
            if side == 0 and rayDirX > 0:
                texX = texWidth - texX - 1
            if side == 1 and rayDirY < 0:
                texX = texWidth - texX - 1
            
            for y in range(texHeight):
                # Ignore pixels that are off of the screen
                if drawStart + (lineHeight / texHeight) * (y + 1) < 0:
                    continue
                if drawStart + (lineHeight / texHeight) * y > HEIGHT:
                    break

                # Load pixel's colour from array
                colour = pygame.Color(texArray[texX][y])

                # Darkens environment with distance
                c = 255.0 - abs(int(rayLength * 32)) * 0.85
                if c < 1:
                    c = 1
                if c > 255:
                    c = 255

                # Different faces have different luminence to add to the 3D effect
                if side == 1:
                    c = c * 0.75

                # Change the luminence if necessary
                new_colour = []
                for i, value in enumerate(colour):
                    if i == 0:
                        continue  # Exclude the alpha value
                    new_colour.append(value * (c / 255))
                colour = tuple(new_colour)
                
                pygame.draw.line(SCREEN, colour, (x, drawStart + (lineHeight / texHeight) * y),
                                 (x, drawStart + (lineHeight / texHeight) * (y + 1)), resolution)

        # Render the HUD
        SCREEN.blit(HUD, (0, HEIGHT))

        # Mini map
        # for x in range(mapBoundX):
        #     for y in range(mapBoundY):
        #         if mapGrid[y][x] != 0:
        #             pygame.draw.rect(SCREEN, map_colour, (
        #             (x * (map_size / mapBoundX) + WIDTH) - map_size,
        #             y * (map_size / mapBoundY) + HEIGHT - map_size, (map_size / mapBoundX),
        #             (map_size / mapBoundY)))
        
        pos_on_map = (posY * (map_size / mapBoundY) + WIDTH - map_size,
                      posX * (map_size / mapBoundX) + HEIGHT - map_size)

        # Draw player on mini map
        pygame.draw.rect(SCREEN, (0, 255, 0), pos_on_map + (2, 2))
        pygame.draw.line(SCREEN, (255, 0, 127), pos_on_map, (
        (dirY + posY + planeY) * (map_size / mapBoundY) + WIDTH - map_size,
        (dirX + posX + planeX) * (map_size / mapBoundX) + HEIGHT - map_size))
        pygame.draw.line(SCREEN, (255, 0, 127), pos_on_map, (
        (dirY + posY - planeY) * (map_size / mapBoundY) + WIDTH - map_size,
        (dirX + posX - planeX) * (map_size / mapBoundY) + HEIGHT - map_size))
        pygame.draw.line(SCREEN, (255, 0, 127), (
        (dirY + posY + planeY) * (map_size / mapBoundY) + WIDTH - map_size,
        (dirX + posX + planeX) * (map_size / mapBoundX) + HEIGHT - map_size), (
                         (dirY + posY - planeY) * (map_size / mapBoundY) + WIDTH - map_size,
                         (dirX + posX - planeX) * (map_size / mapBoundY) + HEIGHT - map_size))

        # Movement controls
        keys = pygame.key.get_pressed()
        
        if keys[K_w]:
            if not mapGrid[int(posX + dirX * move_speed)][int(posY)]:
                posX += dirX * move_speed
            if not mapGrid[int(posX)][int(posY + dirY * move_speed)]:
                posY += dirY * move_speed
        
        if keys[K_a]:
            if not mapGrid[int(posX + dirY * strafe_speed)][int(posY)]:
                posX += dirY * strafe_speed
            if not mapGrid[int(posX)][int(posY - dirX * strafe_speed)]:
                posY -= dirX * strafe_speed
        
        if keys[K_s]:
            if not mapGrid[int(posX - dirX * move_speed)][int(posY)]:
                posX -= dirX * move_speed
            if not mapGrid[int(posX)][int(posY - dirY * move_speed)]:
                posY -= dirY * move_speed
        
        if keys[K_d]:
            if not mapGrid[int(posX - dirY * strafe_speed)][int(posY)]:
                posX -= dirY * strafe_speed
            if not mapGrid[int(posX)][int(posY + dirX * strafe_speed)]:
                posY += dirX * strafe_speed

        # Look left and right
        # Mouse input
        difference = pygame.mouse.get_pos()[0] - (WIDTH / 2)
        pygame.mouse.set_pos([WIDTH / 2, HEIGHT / 2])

        # Keyboard input
        if keys[K_q]:
            difference = -5
        if keys[K_e]:
            difference = 5

        # Vector rotation
        if difference != 0:
            cosrot = cos(difference * rotate_speed)
            sinrot = sin(difference * rotate_speed)
            old = dirX
            dirX = dirX * cosrot - dirY * sinrot
            dirY = old * sinrot + dirY * cosrot
            old = planeX
            planeX = planeX * cosrot - planeY * sinrot
            planeY = old * sinrot + planeY * cosrot
        
        pygame.display.update()
        pygame.display.set_caption(f'{CLOCK.tick(FPS)}')
        


if __name__ == "__main__":
    main()