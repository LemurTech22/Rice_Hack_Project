import pygame
import sys
import math
import random
import assets
from map import TileKind, Map

pygame.init()

screen_width = 1200
screen_height = 800

display = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()

player_walk_images = [pygame.image.load("./assets/player_walk_0.png"), pygame.image.load("./assets/player_walk_1.png"),
pygame.image.load("./assets/player_walk_2.png"), pygame.image.load("./assets/player_walk_3.png")]

player_weapon = pygame.image.load("./assets/shotgun.png").convert()
player_weapon.set_colorkey((255,255,255))

class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.animation_count = 0
        self.moving_right = False
        self.moving_left = False
        #Health
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def handle_weapons(self, display):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        rel_x, rel_y = mouse_x - player.x, mouse_y - player.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

        player_weapon_copy = pygame.transform.rotate(player_weapon, angle)

        display.blit(player_weapon_copy, (self.x+15-int(player_weapon_copy.get_width()/2), self.y+25-int(player_weapon_copy.get_height()/2)))

    def main(self, display):
        if self.animation_count + 1 >= 16:
            self.animation_count = 0

        self.animation_count += 1

        if self.moving_right:
            display.blit(pygame.transform.scale(player_walk_images[self.animation_count//4], (32, 42)), (self.x, self.y))
        elif self.moving_left:
            display.blit(pygame.transform.scale(pygame.transform.flip(player_walk_images[self.animation_count//4], True, False), (32, 42)), (self.x, self.y))
        else:
            display.blit(pygame.transform.scale(player_walk_images[0], (32, 42)), (self.x, self.y))

        self.hitbox.x = self.x
        self.hitbox.y = self.y

        pygame.draw.rect(display, (255,0,0), self.hitbox, 2)

        self.handle_weapons(display)

        self.moving_right = False
        self.moving_left = False


class PlayerBullet:
    def __init__(self, x, y, width, height, mouse_x, mouse_y):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.speed = 15
        self.angle = math.atan2(y - mouse_y, x - mouse_x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed
        # Create hitbox (as a rectangle or bounding box for a circle)
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def main(self, display):
        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)

        # Update hitbox position
        self.hitbox.x = self.x
        self.hitbox.y = self.y

        # Draw the bullet as a circle
        pygame.draw.circle(display, (0, 0, 0), (self.x + self.width // 2, self.y + self.height // 2), 5)

        # Draw the hitbox for debugging purposes (optional)
        self.hitbox = pygame.draw.rect(display, (255, 0, 0), self.hitbox, 2)


class SlimeEnemy:
    def __init__(self, x, y,width, height):
        self.x = x
        self.y = y
        self.animation_images = [pygame.image.load("./assets/slime_animation_0.png"), pygame.image.load("./assets/slime_animation_1.png"),
        pygame.image.load("./assets/slime_animation_2.png"), pygame.image.load("./assets/slime_animation_3.png")]
        self.animation_count = 0
        self.width = width
        self.height = height
        self.reset_offset = 0
        self.offset_x = random.randrange(-300, 300)
        self.offset_y = random.randrange(-300, 300)
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
    def main(self, display):
        if self.animation_count + 1 == 16:
            self.animation_count = 0
        self.animation_count += 1

        if self.reset_offset == 0:
            self.offset_x = random.randrange(-300, 300)
            self.offset_y = random.randrange(-300, 300)
            self.reset_offset = random.randrange(120, 150)
        else:
            self.reset_offset -= 1

        if player.x + self.offset_x > self.x-display_scroll[0]:
            self.x += 1
        elif player.x + self.offset_x < self.x-display_scroll[0]:
            self.x -= 1

        if player.y + self.offset_y > self.y-display_scroll[1]:
            self.y += 1
        elif player.y + self.offset_y < self.y-display_scroll[1]:
            self.y -= 1
        self.hitbox.x = self.x
        self.hitbox.y = self.y
        

        self.hitbox=pygame.draw.rect(display, (255, 0, 0), (self.hitbox.x - display_scroll[0], self.hitbox.y - display_scroll[1], self.width, self.height), 2)
        display.blit(pygame.transform.scale(self.animation_images[self.animation_count//4], (32, 30)), (self.x-display_scroll[0], self.y-display_scroll[1]))



enemies = [SlimeEnemy(400, 300, 32, 30),SlimeEnemy(600, 300, 32, 30)]

player = Player(screen_width/2, screen_height/2, 32, 32)

display_scroll = [0,0]

player_bullets = []

TileKinds = [
    TileKind("dirt", "./assets/dirt.png", False),
    TileKind("grass", "./assets/grass.png", False),
    TileKind("water", "./assets/water.png", False),
    TileKind("wood", "./assets/wood.png", False)
]

# Game running loop
while True:
    map = Map("Levels/testmap.level", TileKinds, 32)
    display.fill((24,164,86))

    mouse_x, mouse_y = pygame.mouse.get_pos()

        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player_bullets.append(
                    PlayerBullet(player.x, player.y, 10, 10, mouse_x, mouse_y))  # Use 10x10 as the size of the bullet

    keys = pygame.key.get_pressed()

    map.draw(display, display_scroll[0], display_scroll[1])

    mapImageTest = pygame.image.load('./assets/player_image.png')

    display.blit(mapImageTest, (-display_scroll[0], -display_scroll[1]))

    pygame.draw.rect(display, (255,255,255), (100-display_scroll[0], 100-display_scroll[1], 100, 100),2)

    player.main(display)

    if keys[pygame.K_a]:
        display_scroll[0] -= 5

        player.moving_left = True

        for bullet in player_bullets:
            bullet.x += 5
    if keys[pygame.K_d]:
        display_scroll[0] += 5

        player.moving_right = True

        for bullet in player_bullets:
            bullet.x -= 5
    if keys[pygame.K_w]:
        display_scroll[1] -= 5

        for bullet in player_bullets:
            bullet.y += 5
    if keys[pygame.K_s]:
        display_scroll[1] += 5

        for bullet in player_bullets:
            bullet.y -= 5

    player.main(display)
    for bullet in player_bullets:
        bullet.main(display)
        if bullet.hitbox.colliderect(enemy.hitbox):
            print("Slime has been shot")
            enemies.remove(enemy)
            player_bullets.remove(bullet)
        
    if enemies:
        for enemy in enemies[:]:
            enemy.main(display)
            if player.hitbox.colliderect(enemy.hitbox):
                print("Collision")

            
    
    clock.tick(60)
    pygame.display.update()