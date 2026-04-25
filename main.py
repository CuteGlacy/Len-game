import pygame
import random
import sys
import os

pygame.init()

#configuración inicial
WIDTH, HEIGHT = 900, 400
FONT= pygame.font.SysFont("arial", 24)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Len Run Adventure")
clock = pygame.time.Clock()

#colores
BG_COLOR = (135, 206, 235)
SAND = (255, 240, 133)
RED = (220, 60, 60)
WHITE = (255, 255, 255)

#carga sprites
DINO_NORMAL_IMG = pygame.image.load(os.path.join("img", "player.png").convert_alpha())
DINO_DUCK_IMG = pygame.image.load(os.path.join("img", "player agachado.png").convert_alpha())
CACTUS_IMG = pygame.image.load(os.path.join("img", "fantasmita.png").convert_alpha())
ROCK_IMG = pygame.image.load(os.path.join("img", "la roca.png").convert_alpha())
CLOUD_IMG = pygame.image.load(os.path.join("img", "nube.png").convert_alpha())
#Escalado sprites
DINO_NORMAL_IMG = pygame.transform.scale(DINO_NORMAL_IMG, (60, 80))
DINO_DUCK_IMG = pygame.transform.scale(DINO_NORMAL_IMG, (60, 40))
CACTUS_IMG = pygame.transform.scale(DINO_NORMAL_IMG, (30, 60))
ROCK_IMG = pygame.transform.scale(DINO_NORMAL_IMG, (40, 40))
CLOUD_IMG = pygame.transform.scale(DINO_NORMAL_IMG, (50, 30))


# Función Principal
def run_game():
    
    #configuración
    player.img = DINO_NORMAL_IMG
    player = pygame.Rect(80, HEIGHT - 120, 60, 80)
    player_vel_y = 0
    gravityt = 0.8
    jump_strength = -15
    on_ground = True
    is_ducking = False
    ground_y = HEIGHT - 40
    obstacles = []
    clouds = []
    spaw_timer = 0
    spawn_delay = 90
    score = 0
    speed = 6
    running = True

    while running:
        clock.tick(60)
        screen.fill(BG_COLOR)



        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.ket.get_pressed()

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and on_ground:
            dino_vel_y = jump_strength
            on_ground = False
        
        if keys[pygame.K_DOWN] and on_ground:
            if not is_ducking:
                player_png = DINO_DUCK_IMG
                player.height = 40
                player.y += 40
                is_ducking = True
            else:
                if is_ducking:
                    player_png = DINO_NORMAL_IMG
                    player.y -= 40
                    player.height = 80
                    is_ducking = False
