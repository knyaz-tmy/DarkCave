import pygame
import sys
import random

WIDTH = 800
HEIGHT = 600
FPS = 80
NormalFPS = 30
gravity = 0.6 / (FPS / NormalFPS)
x_velocity = 8 / (FPS / NormalFPS)
jump_velocity = -18 / (FPS / NormalFPS)

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (0, 0, 255)


def load_and_transform_image(filename, do_flip=False, ratio=5):
    surf = pygame.image.load(filename).convert_alpha()
    surf = pygame.transform.scale(surf, (surf.get_width() * ratio, surf.get_height() * ratio))
    surf = pygame.transform.flip(surf, do_flip, False)
    return surf


class AnimationSprite(pygame.sprite.Sprite):
    def load_animations(self):
        self.animation_frames = {}

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.animation_frames = {}
        self.load_animations()
        self.frame = 0
        self.animation_sequence = ''
        self.animation_speed = 1

    def update(self):
        self.frame += self.animation_speed
        if self.frame >= len(self.animation_frames[self.animation_sequence]):
            self.frame = 0
        self.image = self.animation_frames[self.animation_sequence][int(self.frame)]


class Player(AnimationSprite):

    def load_animations(self):
        self.animation_frames = {'idle_left': [load_and_transform_image("Images/Игрок(стойка)1.png", True),
                                               load_and_transform_image("Images/Игрок(стойка)2.png", True),
                                               load_and_transform_image("Images/Игрок(стойка)3.png", True),
                                               load_and_transform_image("Images/Игрок(стойка)4.png", True),
                                               load_and_transform_image("Images/Игрок(стойка)5.png", True),
                                               load_and_transform_image("Images/Игрок(стойка)6.png", True),
                                               load_and_transform_image("Images/Игрок(стойка)7.png", True),
                                               load_and_transform_image("Images/Игрок(стойка)8.png", True)],
                                 'idle_right': [load_and_transform_image("Images/Игрок(стойка)1.png"),
                                                load_and_transform_image("Images/Игрок(стойка)2.png"),
                                                load_and_transform_image("Images/Игрок(стойка)3.png"),
                                                load_and_transform_image("Images/Игрок(стойка)4.png"),
                                                load_and_transform_image("Images/Игрок(стойка)5.png"),
                                                load_and_transform_image("Images/Игрок(стойка)6.png"),
                                                load_and_transform_image("Images/Игрок(стойка)7.png"),
                                                load_and_transform_image("Images/Игрок(стойка)8.png")],
                                 'run_left': [load_and_transform_image("Images/run1.png", True),
                                              load_and_transform_image("Images/run2.png", True),
                                              load_and_transform_image("Images/run3.png", True),
                                              load_and_transform_image("Images/run4.png", True)],
                                 'run_right': [load_and_transform_image("Images/run1.png"),
                                               load_and_transform_image("Images/run2.png"),
                                               load_and_transform_image("Images/run3.png"),
                                               load_and_transform_image("Images/run4.png")],
                                 'jump_origin_left': [load_and_transform_image("Images/jump1.png", True),
                                                      load_and_transform_image("Images/jump2.png", True)],
                                 'jump_fly_left': [load_and_transform_image("Images/jump3.png", True),
                                                   load_and_transform_image("Images/jump4.png", True), ],
                                 'jump_air_jump_left': [load_and_transform_image("Images/jump2.png", True)],
                                 'jump_y0_left': [load_and_transform_image("Images/jump5.png", True)],
                                 'jump_fall_left': [load_and_transform_image("Images/jump6.png", True),
                                                    load_and_transform_image("Images/jump7.png", True)],
                                 'jump_end_left': [load_and_transform_image("Images/jump8.png", True),
                                                   load_and_transform_image("Images/jump9.png", True)],
                                 'jump_origin_right': [load_and_transform_image("Images/jump1.png"),
                                                       load_and_transform_image("Images/jump2.png")],
                                 'jump_fly_right': [load_and_transform_image("Images/jump3.png"),
                                                    load_and_transform_image("Images/jump4.png")],
                                 'jump_air_jump_right': [load_and_transform_image("Images/jump2.png")],
                                 'jump_y0_right': [load_and_transform_image("Images/jump5.png")],
                                 'jump_fall_right': [load_and_transform_image("Images/jump6.png"),
                                                     load_and_transform_image("Images/jump7.png")],
                                 'jump_end_right': [load_and_transform_image("Images/jump8.png"),
                                                    load_and_transform_image("Images/jump9.png")],
                                 }

    def __init__(self):
        super().__init__()
        self.animation_sequence = 'idle_right'
        self.animation_speed = 15 / FPS  # Частота кадров анимации, деленная на текущий FPS игры
        self.image = self.animation_frames[self.animation_sequence][self.frame]  # TODO: Нужно понять - требуется ли переопределять rect при изменении картинки
        self.rect = self.image.get_rect()
        self.v_sprite = pygame.sprite.Sprite()
        self.v_sprite.rect = self.image.get_rect()
        self.v_sprite.rect.height += 1
        self.yvel = 0
        self.rect.centerx = WIDTH / 2
        self.rect.y = 0
        self.xvel = 0
        self.on_ground = False
        self.max_air_jump = 1
        self.air_jump = self.max_air_jump

    def set_on_ground(self, on_ground):
        if not on_ground and self.animation_sequence == 'run_right':
            self.animation_sequence = 'idle_right'
        elif not on_ground and self.animation_sequence == 'run_left':
            self.animation_sequence = 'idle_left'
        elif on_ground and not self.on_ground and self.xvel > 0:
            self.animation_sequence = 'run_right'
        elif on_ground and not self.on_ground and self.xvel < 0:
            self.animation_sequence = 'run_left'
        self.on_ground = on_ground

    def jump(self):
        if self.air_jump > 0 or self.on_ground:
            if self.xvel > 0:
                self.animation_sequence = 'jump_origin_right'
            else:
                self.animation_sequence = 'jump_origin_left'
            self.yvel = jump_velocity
            if not self.on_ground:
                self.air_jump -= 1
                if self.xvel > 0:
                    self.animation_sequence = 'jump_air_jump_right'
                else:
                    self.animation_sequence = 'jump_air_jump_left'
            self.set_on_ground(False)
            if self.yvel == 0:
                if self.xvel > 0:
                    self.animation_sequence = 'jump_y0_right'
                else:
                    self.animation_sequence = 'jump_y0_left'
            if self.yvel >= -0.1:
                if self.xvel > 0:
                    self.animation_sequence = 'jump_fall_right'
                else:
                    self.animation_sequence = 'jump_fall_left'

    def move_left(self):
        if self.on_ground:
            self.animation_sequence = 'run_left'
        else:
            self.animation_sequence = 'idle_left'
        self.xvel = -x_velocity

    def move_right(self):
        if self.on_ground:
            self.animation_sequence = 'run_right'
        else:
            self.animation_sequence = 'idle_right'
        self.xvel = x_velocity

    def move_stop(self):
        if self.xvel < 0:
            self.animation_sequence = 'idle_left'
        else:
            self.animation_sequence = 'idle_right'
        self.xvel = 0

    def determineSide(self, rect):
        if self.rect.midtop[1] > rect.midtop[1]:
            return "top"
        elif self.rect.midleft[0] > rect.midleft[0]:
            return "left"
        elif self.rect.midright[0] < rect.midright[0]:
            return "right"
        else:
            return "bottom"

    def update(self):
        super().update()
        self.rect.x += self.xvel
        if self.rect.x > WIDTH - self.rect.width:
            self.rect.x = 0
        if self.rect.x < 0:
            self.rect.x = WIDTH - self.rect.width
        self.rect.y += self.yvel
        self.v_sprite.rect.x = self.rect.x
        self.v_sprite.rect.y = self.rect.y
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            if self.xvel > 0:
                self.animation_sequence = 'jump_end_right'
            else:
                self.animation_sequence = 'jump_end_left'
            print(self.determineSide(hits[0].rect))
            self.rect.y = hits[0].rect.top - self.rect.height
            self.v_sprite.rect.x = self.rect.x
            self.v_sprite.rect.y = self.rect.y
            self.set_on_ground(True)
            self.yvel = 0
            self.air_jump = self.max_air_jump
        v_hits = pygame.sprite.spritecollide(self.v_sprite, platforms, False)
        self.on_ground = len(v_hits) > 0
        if not self.on_ground:
            self.yvel += gravity


class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Images/plat1.png")
        self.rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT - self.image.get_height() / 2))


class Platforms(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        super().__init__()
        self.image = pygame.image.load("Images/plat1.png")
        self.rect = self.image.get_rect(left=x, top=y, width=width, height=self.image.get_height())


class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.bg = pygame.image.load('Images/main_game1.gif')
        self.bgRect = (0, 0, WIDTH, HEIGHT)

    def update(self):
        screen.blit(self.bg, self.bgRect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()


def key_event_proccess(key_event):
    if key_event.key == pygame.K_LEFT or key_event.key == pygame.K_a:
        if key_event.type == pygame.KEYDOWN:
            player.move_left()
        else:
            if player.xvel < 0:
                player.move_stop()
    elif key_event.key == pygame.K_RIGHT or key_event.key == pygame.K_d:
        if key_event.type == pygame.KEYDOWN:
            player.move_right()
        else:
            if player.xvel > 0:
                player.move_stop()
    elif key_event.key == pygame.K_UP or key_event.key == pygame.K_w:
        if key_event.type == pygame.KEYDOWN:
            player.jump()


# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
ground = Ground()
platform1 = Platforms(100, 400, 100)
platform2 = Platforms(420, 300, 100)
player = Player()
platforms = pygame.sprite.Group()
platforms.add(platform1, platform2, ground)

all_sprites = pygame.sprite.Group()
all_sprites.add(ground)
all_sprites.add(platform1, platform2)
all_sprites.add(player)

background = Background()

# Главный цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Обработка ввода (события)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP or event.type == pygame.KEYDOWN:
            key_event_proccess(event)
    all_sprites.update()
    screen.fill((0, 0, 0))
    background.update()

    all_sprites.draw(screen)

    pygame.display.update()

pygame.quit()
