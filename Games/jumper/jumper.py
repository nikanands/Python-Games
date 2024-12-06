import pygame, sys
from random import randint, choice
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80,300))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.6)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.jump_sound.play()
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.bottom += self.gravity
        if self.rect.bottom >= 300: self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('graphics/Snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/Snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0

        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900,1000), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    curr_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surf = basic_font.render(f'Score: {curr_time}', True, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return curr_time

# def obstacle_movement(obstacle_list):
#     if obstacle_list:
#         for obstacle_rect in obstacle_list:
#             obstacle_rect.x -= 5
#
#             if obstacle_rect.bottom == 300: screen.blit(snail_surf,obstacle_rect)
#             else: screen.blit(fly_surf, obstacle_rect)
#
#         obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
#
#         return obstacle_list
#
#     else: return []

# def collisions(player, obstacles):
#     if obstacles:
#         for obstacle_rect in obstacles:
#             if player.colliderect(obstacle_rect): return False
#     return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle, False):
        obstacle.empty()
        return False
    else: return True

def terminate():
    pygame.quit()
    sys.exit()

# def player_animation():
#     global player_surf, player_index
#
#     if player_rect.bottom < 300:
#         player_surf = player_jump
#     else:
#         player_index += 0.1
#         if player_index >= len(player_walk): player_index = 0
#         player_surf = player_walk[int(player_index)]


pygame.init()

# CREATE SCORE
score = 0

# CREATE SCREEN
screen = pygame.display.set_mode((800,400))

# CREATE TITLE
pygame.display.set_caption('JUMPING RUNNER')

# BACKGROUND MUSIC
bg_sound = pygame.mixer.Sound('audio/music.wav')
bg_sound.set_volume(0.1)
bg_sound.play(-1)

# CREATE CLOCK
clock = pygame.time.Clock()
start_time = 0

# GAME STATE
game_active = False

# SKY SURFACE
sky_surf = pygame.image.load('graphics/Sky.png').convert()

# GROUND SURFACE
ground_surf = pygame.image.load('graphics/ground.png').convert()

# BASIC FONT
basic_font = pygame.font.Font('Font/Pixeltype.ttf', 50)

# OBSTACLES SURFACE
snail_surf = pygame.image.load('graphics/Snail/snail1.png').convert_alpha()

fly_surf = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()

obstacle_rect_list = []

# PLAYER SURF

# player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
# player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
# player_walk = [player_walk_1,player_walk_2]
# player_index = 0
# player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
# player_surf = player_walk[player_index]
# player_rect = player_surf.get_rect(midbottom=(80,300))
# player_gravity = 0

# INTRO SCREEN
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center=(400,200))
game_name = basic_font.render('JUMPING RUNNER', False, (111,196,169))
game_name_rect = game_name.get_rect(center=(400,80))

game_message = basic_font.render('Press SPACE to start', False, (111,196,169))
game_message_rect = game_message.get_rect(center=(400,330))

# OBSTACLE TIMER
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

# PLAYER GROUP
player = pygame.sprite.GroupSingle()
player.add(Player())

# OBSTACLE GROUP
obstacle = pygame.sprite.Group()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        # if game_active:
            # if event.type == KEYDOWN:
            #     if event.key == K_ESCAPE:
            #         pygame.quit()
            #         sys.exit()
            #     if event.key == K_SPACE and player_rect.bottom >= 300:
            #         player_gravity = -20
            # if event.type == KEYUP:
            #     pass

            # if event.type == MOUSEBUTTONDOWN and player_rect.bottom >= 300:
            #     if player_rect.collidepoint(event.pos):
            #         player_gravity = -20

        else:
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    game_active = True
                    # snail_rect.left = 800
                    start_time = int(pygame.time.get_ticks()/1000)
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        if event.type == obstacle_timer and game_active:
            obstacle.add(Obstacle(choice(['fly', 'snail','snail','snail'])))
            # if randint(0,2):
            #     obstacle_rect_list.append(snail_surf.get_rect(midbottom=(randint(900,1000), 300)))
            # else:
            #     obstacle_rect_list.append(fly_surf.get_rect(midbottom=(randint(900, 1000), 200)))


    if game_active:

        # PLACING THE SKY
        screen.blit(sky_surf, (0,0))
        # PLACING THE GROUND
        screen.blit(ground_surf, (0,300))

        score = display_score()
        # PLACING THE OBSTACLES
        obstacle.draw(screen)
        obstacle.update()
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # PLACING THE PLAYER
        # player_gravity += 1
        # player_rect.y += player_gravity
        # if player_rect.bottom  >= 300: player_rect.bottom= 300
        # player_animation()
        # screen.blit(player_surf,player_rect)
        player.draw(screen)
        player.update()



        # COLLISION
        game_active = collision_sprite()
        # game_active = collisions(player_rect, obstacle_rect_list)

    else:
        screen.fill((94,129,164))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name, game_name_rect)
        obstacle_rect_list.clear()
        # player_rect.midbottom = (80,300)
        player_gravity = 0
        score_msg = basic_font.render(f'Your Score: {score}', False, (111,196,169))
        score_msg_rect = score_msg.get_rect(center=(400,330))

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_msg,score_msg_rect)

    pygame.display.update()
    clock.tick(60)