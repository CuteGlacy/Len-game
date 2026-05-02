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
DINO_NORMAL_IMG = pygame.image.load(os.path.join("player.png")).convert_alpha()
DINO_DUCK_IMG = pygame.image.load(os.path.join("player agachado.png")).convert_alpha()
CACTUS_IMG = pygame.image.load(os.path.join("fantasmita.png")).convert_alpha()
ROCK_IMG = pygame.image.load(os.path.join("la roca.png")).convert_alpha()
CLOUD_IMG = pygame.image.load(os.path.join("nube.png")).convert_alpha()
#Escalado sprites
DINO_NORMAL_IMG = pygame.transform.scale(DINO_NORMAL_IMG, (60, 80))
DINO_DUCK_IMG = pygame.transform.scale(DINO_DUCK_IMG, (60, 40))
CACTUS_IMG = pygame.transform.scale(CACTUS_IMG, (30, 60))
ROCK_IMG = pygame.transform.scale(ROCK_IMG, (40, 40))
CLOUD_IMG = pygame.transform.scale(CLOUD_IMG, (80, 50))


# Función Principal
def run_game():
    
    #configuración
    player_img = DINO_NORMAL_IMG
    player = pygame.Rect(80, HEIGHT - 120, 60, 80)
    player_vel_y = 0
    gravity = 0.8
    jump_strength = -15
    on_ground = True
    is_ducking = False
    ground_y = HEIGHT - 40
    obstacles = []
    birds = []
    spawn_timer = 0
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
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and on_ground:
            player_vel_y = jump_strength
            on_ground = False
        
        if keys[pygame.K_DOWN] and on_ground:
            if not is_ducking:
                player_img = DINO_DUCK_IMG
                player.height = 40
                player.y += 40
                is_ducking = True
        else:
            if is_ducking:
                    player_img = DINO_NORMAL_IMG
                    player.y -= 40
                    player.height = 80
                    is_ducking = False

        player_vel_y += gravity
        player.y += player_vel_y
        if player.bottom >= ground_y:
                    player.bottom = ground_y
                    player_vel_y = 0
                    on_ground = True

        spawn_timer += 1
        if spawn_timer >= spawn_delay:
            choice = random.choice(["fantasma", "roca", "nube"])

            if choice == "fantasma":
                    rect = pygame.Rect(WIDTH + 20, ground_y -60, 30, 60)
                    obstacles.append((rect, CACTUS_IMG))

            elif choice == "roca":
                    rect = pygame.Rect(WIDTH + 20, ground_y - 40, 40, 40)
                    obstacles.append((rect, ROCK_IMG))

            else:
                y = random.choice([ground_y - 100, ground_y - 120])
                bird = pygame.Rect(WIDTH + 20, y, 80, 50)
                birds.append(bird)

            spawn_timer = 0
            if spawn_delay > 50:
                spawn_delay -= 1

        for rect, img in obstacles[:]:
            rect.x -= speed
            if rect.right < 0:
                obstacles.remove((rect, img))
                score += 1

        for bird in birds[:]:
            bird.x -= speed + 2
            if bird.right < 0:
                birds.remove(bird)
                score += 2

        # Update speed
        speed = 6 + score // 20

        # Move obstacles and birds
        for rect, img in obstacles[:]:
            rect.x -= speed
            if rect.right < 0:
                obstacles.remove((rect, img))
                score += 1

        for bird in birds[:]:
            bird.x -= speed + 2
            if bird.right < 0:
                birds.remove(bird)
                score += 2

        # Collision detection
        hit = False
        for rect, img in obstacles:
            if player.colliderect(rect):
                hit = True
                break
        for bird in birds:
            if player.colliderect(bird):
                hit = True
                break
        if hit:
            running = False

        pygame.draw.rect(screen, SAND, (0, ground_y, WIDTH, 40))

        screen.blit(player_img, (player.x, player.y))

        for rect, img in  obstacles:
            screen.blit(img,(rect.x, rect.y))

        for bird in birds:
            screen.blit(CLOUD_IMG, (bird.x, bird.y))

        score_text = FONT.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        high_score_text = FONT.render(f"High: {score}", True, WHITE)
        screen.blit(high_score_text, (10, 40))
        instr_text = FONT.render("SPACE/UP: Jump   DOWN: Duck", True, WHITE)
        screen.blit(instr_text, (10, HEIGHT - 30))

        pygame.display.flip()

    while True:
        screen.fill(BG_COLOR)
        over_text = FONT.render("GAME OVER", True, RED)
        score_text = FONT.render(f"Final Score: {score}", True, WHITE)
        restart_text = FONT.render("Press R to Restart", True, WHITE)

        screen.blit(over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 40))
        screen.blit(score_text, (WIDTH // 2 - 110, HEIGHT // 2))
        high_score_text = FONT.render(f"High Score: {score}", True, WHITE)
        screen.blit(high_score_text, (WIDTH // 2 - 120, HEIGHT // 2 - 20))
        screen.blit(restart_text, (WIDTH // 2 - 130, HEIGHT // 2 + 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return score
                

while True:
    final_score = run_game()
