import pygame
import sys
import math
import random
import assets

pygame.init()

screen_width = 1200
screen_height = 800
# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
display = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()

player_walk_images = [pygame.image.load("./assets/player_walk_0.png"), pygame.image.load("./assets/player_walk_1.png"),
pygame.image.load("./assets/player_walk_2.png"), pygame.image.load("./assets/player_walk_3.png")]

player_weapon = pygame.image.load("./assets/shotgun.png").convert()
player_weapon.set_colorkey((255,255,255))

font = pygame.font.Font(None,36)

def start_screen():
    # Set up the font for the title
    title_font = pygame.font.Font(None, 74)
    instruction_font = pygame.font.Font(None, 36)

    # Render the title and instruction text
    title_text = title_font.render("Your Game Title", True, WHITE)
    instruction_text = instruction_font.render("Press any key to start", True, WHITE)

    # Center the text on the screen
    title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    instruction_rect = instruction_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))

    # Display the start screen until a key is pressed
    while True:
        display.fill((0, 0, 0))  # Fill the screen with black
        display.blit(title_text, title_rect)  # Draw the title text
        display.blit(instruction_text, instruction_rect)  # Draw the instruction text

        # Check for key press event to start the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return  # Exit the start screen function to start the game

        # Update the display and control the frame rate
        pygame.display.update()
        clock.tick(60)

# Define the rest of your classes and game functions (Player, SlimeEnemy, etc.)

# Call the start screen before the main game loop
start_screen()


class Boss:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = 30  # Boss requires 30 hits to die
        self.animation_images = [
            pygame.image.load("./Characters/Enemies/Boss1.png"),
            pygame.image.load("./Characters/Enemies/Boss2.png")
        ]
        self.animation_count = 0
        self.reset_offset = 0
        self.offset_x = random.randrange(-300, 300)
        self.offset_y = random.randrange(-300, 300)
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.bullets = []
        self.bullet_cooldown = 0  # Control bullet shooting speed

    def follow_player(self):
        if self.reset_offset == 0:
            self.offset_x = random.randrange(-300, 300)
            self.offset_y = random.randrange(-300, 300)
            self.reset_offset = random.randrange(120, 150)
        else:
            self.reset_offset -= 1

        if player.x + self.offset_x > self.x - display_scroll[0]:
            self.x += 1
        elif player.x + self.offset_x < self.x - display_scroll[0]:
            self.x -= 1

        if player.y + self.offset_y > self.y - display_scroll[1]:
            self.y += 1
        elif player.y + self.offset_y < self.y - display_scroll[1]:
            self.y -= 1

    def shoot(self, player):
        if self.bullet_cooldown == 0:
            # Boss shoots three bullets in different directions
            angles = [-0.2, 0, 0.2]  # Spread shot pattern
            for angle in angles:
                bullet = BossBullet(self.x, self.y, player.x, player.y, angle)
                self.bullets.append(bullet)
            self.bullet_cooldown = 60  # Cooldown time before next shot
        else:
            self.bullet_cooldown -= 1

    def main(self, display, player):
        # Update boss animation
        if self.animation_count + 1 >= 16:
            self.animation_count = 0
        self.animation_count += 1

        display.blit(pygame.transform.scale(self.animation_images[self.animation_count // 8], (self.width, self.height)), (self.x - display_scroll[0], self.y-display_scroll[1]))

        # Boss follows the player
        self.follow_player()

        # Boss shoots bullets
        self.shoot(player)

        # Update bullets and draw them
        for bullet in self.bullets[:]:
            bullet.main(display)
            if bullet.hitbox.colliderect(player.hitbox):
                player.take_hit()  # Player takes damage if hit
                self.bullets.remove(bullet)

        # Update hitbox position
        self.hitbox.x = self.x
        self.hitbox.y = self.y
class BossBullet:
    def __init__(self, x, y, target_x, target_y, angle_offset=0):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.speed = 7
        self.angle = math.atan2(target_y - y, target_x - x) + angle_offset
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def main(self, display):
        self.x += int(self.x_vel)
        self.y += int(self.y_vel)

        # Draw the bullet as a red circle
        pygame.draw.circle(display, (255, 0, 0), (self.x, self.y), 5)

        # Update hitbox position
        self.hitbox.x = self.x
        self.hitbox.y = self.y

# Function to spawn the boss
def spawn_boss():
    x = random.randint(0, screen_width - 100)
    y = random.randint(0, screen_height - 100)
    return Boss(x, y, 400, 400)

boss = None
boss_active = False

class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = 3
        self.immune = False
        self.immune_timer = 0
        self.animation_count = 0
        self.moving_right = False
        self.moving_left = False
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

    def take_hit(self):
        if not self.immune:
            self.health -= 1
            self.immune = True
            self.immune_timer = pygame.time.get_ticks()

    def check_immunity(self):
        if self.immune:
            current_time = pygame.time.get_ticks()
            if current_time - self.immune_timer > 4000:
                self.immune = False

    def draw_health_bar(self, display):
        for i in range(self.health):
            pygame.draw.rect(display, (255, 0, 0), (20 + i * 40, 20, 30, 30))


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

def start_new_round(current_round):
    number_of_enemies = current_round * 2  # Increase enemies with each round
    new_enemies = []
    for _ in range(number_of_enemies):
        x = random.randint(0, screen_width - 50)
        y = random.randint(0, screen_height - 50)
        new_enemies.append(SlimeEnemy(x, y, 50, 50))
    return new_enemies

# Function to check if the round is complete (all enemies are defeated)
def check_round_completion(enemies):
    if len(enemies) == 0:  # All enemies defeated
        return True
    return False


# Function to display the current round information
def display_round_info(display, current_round):
    round_text = font.render(f"Round: {current_round}", True, (0, 0, 0))
    display.blit(round_text, (screen_width - 150, 20))

def spawn_Enemy():
    x = random.randint(0,screen_width-50)
    y = random.randint(0,screen_height-50)
    enemy = SlimeEnemy(x, y, 32, 30)
    enemies.append(enemy)

enemies = [SlimeEnemy(400, 300, 32, 30),SlimeEnemy(600, 300, 32, 30)]

player = Player(screen_width/2, screen_height/2, 32, 32)
current_round = 6
enemies = start_new_round(current_round)
max_rounds = 6
display_scroll = [0,0]
round_over = False
player_bullets = []
spawn_timer = 0
bulletTime = 0
# Game running loop
# Main game loop
#Game running loop
while True:
    if bulletTime >= 30:
        bulletTime = 1
    bulletTime += 1
    display.fill((0, 0, 0))

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.quit()

    # Player can shoot regardless of whether the boss is active or not
    if bulletTime % 20 == 1:
        player_bullets.append(PlayerBullet(player.x + 10, player.y + 10, 10, 10, mouse_x, mouse_y))

    keys = pygame.key.get_pressed()

    mlback = pygame.image.load("./Levels/MLBACK.png")
    display.blit(pygame.transform.scale(mlback, (2.13 * screen_width, 2.2 * screen_height)),
                 ((550 - screen_width) - display_scroll[0], (350 - screen_height) - display_scroll[1]))

    player.main(display)

    # Player movement
    if keys[pygame.K_a]:
        if display_scroll[0] > -screen_width:
            display_scroll[0] -= 5
        player.moving_left = True
    if keys[pygame.K_d]:
        if display_scroll[0] < screen_width:
            display_scroll[0] += 5
        player.moving_right = True
    if keys[pygame.K_w]:
        if display_scroll[1] > -screen_height:
            display_scroll[1] -= 5
    if keys[pygame.K_s]:
        if display_scroll[1] < screen_height:
            display_scroll[1] += 5

    # Enemy and bullet handling
    for bullet in player_bullets[:]:
        bullet.main(display)
        if enemies:
            for enemy in enemies[:]:
                if bullet.hitbox.colliderect(enemy.hitbox):
                    print("Slime has been shot")
                    enemies.remove(enemy)
                    if bullet in player_bullets:
                        player_bullets.remove(bullet)
                    break

    if enemies and not boss_active:
        player.check_immunity()
        for enemy in enemies[:]:
            enemy.main(display)
            if player.hitbox.colliderect(enemy.hitbox):
                player.take_hit()
                print("Collision")

    display_round_info(display, current_round)

    # Round progression and boss spawn at round 6
    if not enemies and not round_over and not boss_active:
        round_over = True
        if current_round < max_rounds:
            current_round += 1
            pygame.time.delay(1000)  # Short delay before new round
            enemies = start_new_round(current_round)
            round_over = False
        elif current_round == 6 and not boss_active:  # Boss spawns during round 6
            print("Spawning boss...")
            boss = spawn_boss()  # Random boss spawn
            boss_active = True
            enemies = []  # Clear out other enemies when the boss spawns

    if boss_active:
        boss.main(display, player)  # Render boss and handle movement

        # Check if the boss is hit by player bullets
        for bullet in player_bullets[:]:
            if bullet.hitbox.colliderect(boss.hitbox):
                boss.health -= 1
                player_bullets.remove(bullet)
                print(f"Boss hit! Health left: {boss.health}")

            if boss.health <= 0:
                print("Boss defeated!")
                boss_active = False
                boss = None  # Remove boss after death

        # Check if the boss is colliding with the player (melee hit or close contact)
        if boss.hitbox.colliderect(player.hitbox):
            player.health -= 1
            print(f"I've been hit by the boss")

        # Check if any of the boss's bullets hit the player
        for boss_bullet in boss.bullets[:]:
            if boss_bullet.hitbox.colliderect(player.hitbox):
                player.health -= 1
                boss.bullets.remove(boss_bullet)  # Remove the bullet after it hits the player
                print(f"Player hit by boss's bullet! Health left: {player.health}")


        # Display boss health on the screen
        boss_health_text = font.render(f"Boss Health: {boss.health}", True, (255, 255, 255))
        display.blit(boss_health_text, (20, 50))

    # Game over logic
    if player.health <= 0:
        print("Game Over")
        pygame.quit()
        sys.exit()

    player.draw_health_bar(display)
    clock.tick(60)
    pygame.display.update()