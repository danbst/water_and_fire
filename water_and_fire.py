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
            dt = clock.tick(60)
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
1 0 0 0 2 0 0 0 0 0 2 0 0 0 0 1
1 0 0 0 2 0 0 3 0 0 2 0 0 0 0 1
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
   '0': (0, 0, 0),
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
play_sprite = pygame.image.load('./assets/play.png')
fire_sprite = pygame.image.load('./assets/Огонь2.0.png')
water_sprite = pygame.image.load('./assets/water.png')
# маштабування спрайтів у нові розміри
fire_scaled = pygame.transform.smoothscale(fire_sprite, (BLOCK_WIDTH, BLOCK_HEIGHT))
water_scaled = pygame.transform.smoothscale(water_sprite, (BLOCK_WIDTH, BLOCK_HEIGHT))

SPRITES = dict(
    fire = fire_scaled,
    water = water_scaled,
)

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, c):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.image.fill(BLOCK_COLORS[c])
        self.rect = pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)

def create_level(level):
    entities = pygame.sprite.Group()
    rows = level.lstrip().rstrip().split('\n')
    for y, row in enumerate(rows):
        for x, block in enumerate(row.split(' ')):
            if block in "01":
               b = Block(x*BLOCK_WIDTH, y*BLOCK_HEIGHT, block)
               entities.add(b)
            elif block == "6":
                fire_hero.setpos(x*BLOCK_WIDTH, y*BLOCK_HEIGHT)
            elif block == "5":
                water_hero.setpos(x*BLOCK_WIDTH, y*BLOCK_HEIGHT)
    return entities

MOVE_SPEED = 10
JUMP_POWER = 10
GRAVITY = 0.35

class Player(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, img=None, color=None):
        pygame.sprite.Sprite.__init__(self)
        self.xvel = 0
        self.yvel = 0
        if img:
            self.image = img
        elif color:
            self.image = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
            self.image.fill(color)
        self.rect = pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT) # прямоугольный объект

    def setpos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self, left, right):
        if left:
            self.xvel = -MOVE_SPEED # Лево = x- n
 
        if right:
            self.xvel = MOVE_SPEED # Право = x + n
         
        if not(left or right): # стоим, когда нет указаний идти
            self.xvel = 0

        self.rect.x += self.xvel # переносим свои положение на xvel 
   
    def draw(self, screen): # Выводим себя на экран
        screen.blit(self.image, (self.rect.x, self.rect.y))

fire_hero = Player(img=SPRITES['fire'])
water_hero = Player(img=SPRITES['water'])

def update(dt, keys):
    display.fill((0,0,0))

    fire_hero.update(keys[pygame.K_a], keys[pygame.K_d])
    water_hero.update(keys[pygame.K_LEFT], keys[pygame.K_RIGHT])
    entities.draw(display)
    fire_hero.draw(display)
    water_hero.draw(display)

entities = create_level(level2)
game()
