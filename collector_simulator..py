import os
import random
import sys

import pygame

pygame.init()
size = width, height = 800, 550

pygame.display.set_caption('Collector simulator')
pygame.key.set_repeat(200, 300)
FPS = 50
WIDTH = 500
HEIGHT = 500
STEP = 10
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
level_list = ['level1.txt', 'level2.txt', 'level3.txt', 'level4.txt', 'level5.txt']
items = ['axe.png', 'ring.png', 'sword.png', 'spear.png', 'crown.png']
sp = []
level = 4
stage = 570


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    global level_map
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    random.shuffle(items)
    global stage
    posl = range(11)
    cords = []
    for i in range(5):
        flag = True
        while flag:
            k = random.choice(posl)
            w = random.choice(posl)
            if level[k][w] == '.' and (k, w) not in cords:
                cords.append((k, w))
                flag = False

    item_qa = 0
    item_num = 0
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
                if item_qa < 5:
                    Item(cords[item_num][1], cords[item_num][0], items[item_num])
                    first = Item(cords[item_num][1], cords[item_num][0], items[item_num])
                    Item.dvish(first, stage, 30)
                    item_qa += 1
                    item_num += 1
                    stage += 50
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(name, flag=False):
    intro_text = ["Правила игры",
                  "1. Собери предметы в правильном порядке",
                  "2. Успей за 30 секунд"]

    fon = pygame.transform.scale(load_image(name), (800, 550))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    if flag is True:
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


tile_images = {'wall': load_image('stena.png'), 'empty': load_image('pol.png')}
player_image = load_image('player.png', -1)
tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, x, y):
        if 0 <= self.rect.y + y < height and 0 <= self.rect.x + x < width and \
                level_map[(self.rect.y + y) // tile_height][(self.rect.x + x) // tile_width] in (
                '.', '@'):
            self.rect = self.rect.move(x, y)


class Item(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, name):
        self.sp = sp
        self.name = name
        super().__init__(item_group, all_sprites)
        self.image = load_image(self.name, -1)
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if pygame.sprite.spritecollideany(self, player_group):
            self.sp.append(self.name)
            self.rect = self.image.get_rect().move(800, 30)
            self.image.set_colorkey((255, 255, 255))
            # print(self.sp)

    def dvish(self, x, y):
        self.rect = self.image.get_rect().move(x, y)


start_screen('game design.jpg')
start_screen('fon2.jpg', True)

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()

level_map = None
player, level_x, level_y = generate_level(load_level(level_list[level]))
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        key = pygame.key.get_pressed()
        if key[pygame.K_DOWN]:
            player.update(0, tile_height)
        if key[pygame.K_UP]:
            player.update(0, -tile_height)
        if key[pygame.K_LEFT]:
            player.update(-tile_width, 0)
        if key[pygame.K_RIGHT]:
            player.update(tile_width, 0)

        if bool(sp) is True and sp[:len(sp)] != items[:len(sp)]:
            start_screen('fon3.jpg')
            terminate()
        else:
            if len(sp) == len(items):
                level += 1
                stage = 570
                pygame.sprite.Group.empty(tiles_group)
                pygame.sprite.Group.empty(player_group)
                pygame.sprite.Group.empty(item_group)
                if level > len(level_list) - 1:
                    start_screen('fon4.jpg')
                    terminate()
                player, level_x, level_y = generate_level(load_level(level_list[level]))
                del sp[:]
    item_group.update()
    screen.fill((0, 0, 0))
    tiles_group.draw(screen)
    item_group.draw(screen)
    player_group.draw(screen)

    pygame.display.flip()
terminate()
