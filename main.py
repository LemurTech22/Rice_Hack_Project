import pygame
import sys
import math
import random
import assets

pygame.init()

screen_width = 1200
screen_height = 800
unit_width = 45
unit_height = 40
playerWidth = 64
playerHeight = 64
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


        playerWeaponAngle = pygame.transform.scale(player_weapon, (45,25))

        player_weapon_copy = pygame.transform.rotate(playerWeaponAngle, angle)

        display.blit(player_weapon_copy, (self.x+(self.width/2)-int(player_weapon_copy.get_width()/2), self.y+15+(self.height/2)-int(player_weapon_copy.get_height()/2)))

    def main(self, display):
        if self.animation_count + 1 >= 16:
            self.animation_count = 0

        self.animation_count += 1

        if self.moving_right:
            display.blit(pygame.transform.scale(player_walk_images[self.animation_count//4], (self.width, self.height)), (self.x, self.y))
        elif self.moving_left:
            display.blit(pygame.transform.scale(pygame.transform.flip(player_walk_images[self.animation_count//4], True, False), (self.width, self.height)), (self.x, self.y))
        else:
            display.blit(pygame.transform.scale(player_walk_images[self.animation_count//4], (self.width, self.height)), (self.x, self.y))

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
    def __init__(self, x, y,width, height, enemyType):
        self.x = x
        self.y = y
        if enemyType:
            self.animation_images = [pygame.image.load("./Characters/Enemies/Phantom1.png"), pygame.image.load("./Characters/Enemies/Phantom2.png"), pygame.image.load("./Characters/Enemies/Phantom3.png"), pygame.image.load("./Characters/Enemies/Phantom4.png"), pygame.image.load("./Characters/Enemies/Phantom5.png")]
        else:
            self.animation_images = [pygame.image.load("./Characters/Enemies/pixil-frame-0.png"), pygame.image.load("./Characters/Enemies/pixil-frame-1.png"), pygame.image.load("./Characters/Enemies/pixil-frame-2.png"), pygame.image.load("./Characters/Enemies/pixil-frame-3.png"), pygame.image.load("./Characters/Enemies/pixil-frame-1.png")]
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
        display.blit(pygame.transform.scale(self.animation_images[self.animation_count//4], (self.width, self.height)), (self.x-display_scroll[0], self.y-display_scroll[1]))

def start_new_round(current_round):
    number_of_enemies = current_round * 2  # Increase enemies with each round
    new_enemies = []
    for index in range(number_of_enemies):
        x = random.randint(0, screen_width - 50)
        y = random.randint(0, screen_height - 50)
        new_enemies.append(SlimeEnemy(x, y, 50, 50, index%2==1))
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

def spawn_Enemy(enType):
    x = random.randint(0,screen_width-50)
    y = random.randint(0,screen_height-50)
    enemy = SlimeEnemy(x, y, unit_width, unit_height, enType)
    enemies.append(enemy)

enemies = [SlimeEnemy(400, 300, unit_width, unit_height, True),SlimeEnemy(600, 300, unit_width, unit_height,False)]

player = Player(screen_width/2, screen_height/2, playerWidth, playerHeight)
current_round = 1
enemies = start_new_round(current_round)
max_rounds = 5
display_scroll = [0,0]
round_over = False
player_bullets = []
spawn_timer = 0
bulletTime=0
# Game running loop
while True:
    if bulletTime >=30:
        bulletTime = 1
    bulletTime += 1
    display.fill((0,0,0))

    mouse_x, mouse_y = pygame.mouse.get_pos()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.quit()

    if bulletTime%20 == 1:
        player_bullets.append(PlayerBullet(player.x+(player.width/2), player.y+(player.height/2), 10, 10, mouse_x, mouse_y))  # Use 10x10 as the size of the bullet

    keys = pygame.key.get_pressed()

    mlback = pygame.image.load("./Levels/MLBACK.png")
    display.blit(pygame.transform.scale(mlback,(2.13*screen_width,2.2*screen_height)), ((550-screen_width)-display_scroll[0],(350-screen_height)-display_scroll[1]))
    #display.blit(pygame.transform.scale(self.animation_images[self.animation_count//4], (unit_width, unit_height)), (self.x-display_scroll[0], self.y-display_scroll[1]))


    player.main(display)

    if keys[pygame.K_a]:
        if display_scroll[0] > -screen_width:
            display_scroll[0] -= 5

        player.moving_left = True

        for bullet in player_bullets:
            bullet.x += 5
    if keys[pygame.K_d]:
        if display_scroll[0] < screen_width:
            display_scroll[0] += 5

        player.moving_right = True

        for bullet in player_bullets:
            bullet.x -= 5
    if keys[pygame.K_w]:
        if display_scroll[1] > -screen_height:
            display_scroll[1] -= 5

        for bullet in player_bullets:
            bullet.y += 5
    if keys[pygame.K_s]:
        if display_scroll[1] < screen_height:
            display_scroll[1] += 5

        for bullet in player_bullets:
            bullet.y -= 5
    spawn_timer +=1
    if(spawn_timer > 200):
        spawn_Enemy(bulletTime%3==1)
        spawn_timer=0

   # player.main(display)
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


        for enemy in enemies[:]:
            if bullet.hitbox.colliderect(enemy.hitbox):
                print("Slime has been shot")
                enemies.remove(enemy)
                player_bullets.remove(bullet)
                break

    if enemies:
        player.check_immunity()
        for enemy in enemies[:]:
            enemy.main(display)
            if player.hitbox.colliderect(enemy.hitbox):
                player.take_hit()
                print("Collision")

    display_round_info(display, current_round)

    if not enemies and not round_over:
        round_over = True
        if current_round < max_rounds:
            current_round += 1
            pygame.time.delay(1000)  # Short delay before new round
            enemies = start_new_round(current_round)
            round_over = False
        else:
            print("All rounds completed! You win!")
            pygame.quit()
            sys.exit()

    if player.health <= 0:
        print("Game Over")
        pygame.quit()
        sys.exit()


    player.draw_health_bar(display)
    clock.tick(60)
    pygame.display.update()