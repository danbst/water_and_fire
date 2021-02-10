# Inspired by https://habr.com/ru/post/193888/

import pygame
import random

width = 1000
height = 450
display = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

def game():
    try:
        run = True
        while run:
            dt = clock.tick(25)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    run = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                run = False

            update(dt, keys)
            
            pygame.display.flip()
    except KeyboardInterrupt:
        return
    except:
        pygame.quit()
        raise

    print("Finish")
    pygame.quit()

level1 = """
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
1 5 0 0 2 0 0 3 0 0 2 0 0 0 6 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
"""

level2 = """
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 0 0 0 0 6 1 5 0 0 0 1 0 0 0 1
1 7 3 1 1 1 1 0 0 3 0 1 0 0 0 1
1 7 3 0 0 1 1 1 1 1 0 1 0 0 0 1
1 7 0 3 3 1 0 0 0 3 0 3 0 0 0 1
1 7 0 0 0 3 3 0 0 3 0 0 0 0 0 1
1 1 1 1 0 0 0 0 0 0 0 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
"""

def draw_level(level):
    sprites = {
      "0": "  ",
      "1": "██",
      "2": "UU",
      "3": "\x1b[0;31m╳╳",
      "4": "  ",
      "5": "SS",
      "6": "FF",
      "7": "OO"
    }
    end = "\x1b[0;0m"
    result = ""
    for line in level.split("\n"):
        for sprite_id in line.split(" "):
            if sprite_id != "":
                result += sprites[sprite_id] + end
        result += "\n"
    print(result)

BLOCK_WIDTH = 64
BLOCK_HEIGHT = 64
BLOCK_COLORS = {
   '0': (0, 0, 0, 0),
   '1': (50, 50, 50),
   '2': (0, 255, 0),
   '3': (0, 0, 255),
   '4': (128, 128, 0),
   '5': (0, 128, 128),
   '6': (128, 0, 128),
   '7': (255, 0, 255),
   '8': (255, 255, 0),
}

# підключення спрайтів
pygame.mixer.init(frequency=32000, size=8)
play_sprite = pygame.image.load('./assets/play.png')
fire_sprite = pygame.image.load('./assets/Огонь2.0.png')
water_sprite = pygame.image.load('./assets/water.png')
watert_sprite = pygame.image.load('./assets/water.png')
bg_sprite = pygame.image.load('./assets/bg.png')
# маштабування спрайтів у нові розміри
fire_scaled = pygame.transform.smoothscale(fire_sprite, (int(BLOCK_WIDTH*0.6), int(BLOCK_HEIGHT*0.8)))
water_scaled = pygame.transform.smoothscale(water_sprite, (int(BLOCK_WIDTH*0.6), int(BLOCK_HEIGHT*0.8)))
watert_scaled = pygame.transform.smoothscale(watert_sprite, (int(BLOCK_WIDTH*0.6), int(BLOCK_HEIGHT*0.8)))
bg_scaled = pygame.transform.smoothscale(bg_sprite, (int(BLOCK_WIDTH*20), int(BLOCK_HEIGHT*15)))
## тест розмірів спрайту
#water_scaled.fill((0,0,255))

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init(frequency=44100, size=16)

ASSETS = dict(
    fire = fire_scaled,
    water = water_scaled,
    watert = watert_scaled,
    bg = bg_scaled,
    boom = pygame.mixer.Sound('./assets/bom.wav'),
    coin = pygame.mixer.Sound('./assets/Coin6.wav'),
    jump = pygame.mixer.Sound('./assets/jump.wav'),
)

ASSETS['boom'].set_volume(0.1)
ASSETS['coin'].set_volume(0.1)
ASSETS['jump'].set_volume(0.1)


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, c):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.image.fill(BLOCK_COLORS[c])
        self.rect = pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)

def create_level(level):
    entities = pygame.sprite.Group()
    entities.add(bg_hero)
    platforms = []
    rows = level.lstrip().rstrip().split('\n')
    for y, row in enumerate(rows):
        for x, block in enumerate(row.split(' ')):
            if block == '3':
               y += 0.5
            b = Block(x*BLOCK_WIDTH, y*BLOCK_HEIGHT, block)
            if block != '0':
                entities.add(b)
            b.type = block
            if block not in '560':
                platforms.append(b)
            if block == "6":
                fire_hero.setpos(x*BLOCK_WIDTH, y*BLOCK_HEIGHT)
            elif block == "5":
                water_hero.setpos(x*BLOCK_WIDTH, y*BLOCK_HEIGHT)
                watert_hero.setpos(x*BLOCK_WIDTH, y*BLOCK_HEIGHT)
                bg_hero.setpos(0*BLOCK_WIDTH, 0*BLOCK_HEIGHT)
    return entities, platforms

MOVE_SPEED = 5
AMOVE_SPEED = 100
JUMP_POWER = 13
GRAVITY = 2.0

class Player(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, img=None, color=None):
        pygame.sprite.Sprite.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        if img:
            self.image = img
        elif color:
            self.image = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
            self.image.fill(color)
        self.rect = pygame.Rect(x, y, *self.image.get_size()) # прямоугольный объект

    def setpos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self, left, right, up, platforms):
        if left:
            water_hero.xvel = -MOVE_SPEED # Лево = x- n
 
        if right:
            water_hero.xvel = MOVE_SPEED # Право = x + n
            
        if left:
            fire_hero.xvel = -AMOVE_SPEED # Лево = x- n
 
        if right:
            fire_hero.xvel = AMOVE_SPEED # Право = x + n

        if up:
           if self.onGround: # прыгаем, только когда можем оттолкнуться от земли
               self.yvel = -JUMP_POWER
               self.onGround = False

        if not(left or right): # стоим, когда нет указаний идти
            self.xvel = 0

        if not self.onGround:
            if self.collisions == True:
                self.yvel +=  GRAVITY

        self.onGround = False
        self.rect.x += self.xvel # переносим свои положение на xvel 
        self.collide(self.xvel, 0, platforms)
        self.rect.y += self.yvel # переносим свои положение на xvel 
        self.collide(0, self.yvel, platforms)

    def collide(self, xvel, yvel, platforms):
        if not self.collisions:
           return
        for p in platforms:
            if p.type not in '123':
                continue
            if pygame.sprite.collide_rect(self, p): # если есть пересечение платформы с игроком
                if xvel > 0:                      # если движется вправо
                    self.rect.right = p.rect.left # то не движется вправо
                if xvel < 0:                      # если движется влево
                    self.rect.left = p.rect.right # то не движется влево
                if yvel > 0 and p.rect.y > self.rect.y:                      # если падает вниз
                    if self.yvel > GRAVITY*10:
                        if self == water_hero:
                            ASSETS['coin'].play()
                        else:
                            ASSETS['jump'].play()
                    self.rect.bottom = p.rect.top # то не падает вниз
                    self.onGround = True          # и становится на что-то твердое
                    self.yvel = 0                 # и энергия падения пропадает
                if yvel < 0:                      # если движется вверх
                    self.rect.top = p.rect.bottom+5 # то не движется вверх
                    self.yvel = 0                 # и энергия прыжка пропадает
 
    def draw(self, screen): # Выводим себя на экран
        screen.blit(self.image, (self.rect.x, self.rect.y))

def update(dt, keys):
    display.fill((0,0,0))

    fire_hero.update(keys[pygame.K_a], keys[pygame.K_d], keys[pygame.K_SPACE], platforms)
    water_hero.update(keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_UP], platforms)
    watert_hero.update(keys[pygame.K_f], keys[pygame.K_h], keys[pygame.K_b], platforms)
    bg_hero.update(keys[pygame.K_u], keys[pygame.K_i], keys[pygame.K_o], platforms)

    entities.draw(display)

fire_hero = Player(img=ASSETS['fire'])
water_hero = Player(img=ASSETS['water'])
watert_hero = Player(img=ASSETS['watert'])
bg_hero = Player(img=ASSETS['bg'])

entities, platforms = create_level(level1)

entities.add(fire_hero)
entities.add(water_hero)
entities.add(watert_hero)
water_hero.collisions = True
fire_hero.collisions = True
watert_hero.collisions = True
bg_hero.collisions = False

game()
