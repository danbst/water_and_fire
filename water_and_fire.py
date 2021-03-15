# Inspired by https://habr.com/ru/post/193888/

import pygame
import random

width = 1000
height = 450
display = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

buttons = []
interface_group = pygame.sprite.Group()

def game():
    try:
        run = True
        while run:
            dt = clock.tick(60)
            clicked_buttons = []
            for e in pygame.event.get():
                if e.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    clicked_buttons = [s for s in buttons if s.rect.collidepoint(pos)]
                if e.type == pygame.QUIT:
                    run = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                run = False

            update(dt, keys, clicked_buttons)
            
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
fire_scaled = pygame.transform.smoothscale(fire_sprite, (int(BLOCK_WIDTH*0.8), int(BLOCK_HEIGHT*0.8)))
water_scaled = pygame.transform.smoothscale(water_sprite, (int(BLOCK_WIDTH*0.8), int(BLOCK_HEIGHT*0.8)))
## тест розмірів спрайту
#water_scaled.fill((0,0,255))

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init(frequency=44100, size=16)

ASSETS = dict(
    fire = fire_scaled,
    water = water_scaled,
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

class Button(pygame.sprite.Sprite):
    def __init__(self, name, x, y, color):
        pygame.sprite.Sprite.__init__(self)
        button_width = 400
        button_height = 50
        self.image = pygame.Surface((button_width, button_height))
        self.image.fill(color)
        self.rect = pygame.Rect(x, y, button_width, button_height)
        self.name = name

def create_level(level):
    entities = pygame.sprite.Group()
    platforms = []
    rows = level.lstrip().rstrip().split('\n')
    for y, row in enumerate(rows):
        for x, block in enumerate(row.split(' ')):
            b = Block(x*BLOCK_WIDTH, y*BLOCK_HEIGHT, block)
            entities.add(b)
            b.type = block
            if block not in '560':
                platforms.append(b)
            if block == "6":
                fire_hero.setpos(x*BLOCK_WIDTH, y*BLOCK_HEIGHT)
            elif block == "5":
                water_hero.setpos(x*BLOCK_WIDTH, y*BLOCK_HEIGHT)
    return entities, platforms

MOVE_SPEED = 10
JUMP_POWER = 20
GRAVITY = 1.0

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
            self.xvel = -MOVE_SPEED # Лево = x- n
 
        if right:
            self.xvel = MOVE_SPEED # Право = x + n

        if up:
           if self.onGround: # прыгаем, только когда можем оттолкнуться от земли
               self.yvel = -JUMP_POWER
               self.onGround = False

        if not(left or right): # стоим, когда нет указаний идти
            self.xvel = 0

        if not self.onGround:
            self.yvel +=  GRAVITY

        self.onGround = False
        self.rect.x += self.xvel # переносим свои положение на xvel 
        self.collide(self.xvel, 0, platforms)
        self.rect.y += self.yvel # переносим свои положение на xvel 
        self.collide(0, self.yvel, platforms)

    def collide(self, xvel, yvel, platforms):
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

def update(dt, keys, clicked_buttons):
    display.fill((0,0,0))

    has_changed = handle_menu(keys, clicked_buttons)

    if current_interface == "MAIN_MENU":
        if has_changed:
            buttons.clear()
            interface_group.empty()
            buttons.append(Button("Рівні", 100, 50, (0, 255, 0)))
            buttons.append(Button("Settings", 100, 150, (255, 255, 0)))
            buttons.append(Button("Donut", 100, 250, (255, 0, 0)))
            buttons.append(Button("Exit", 100, 350, (255, 0, 255)))
            interface_group.add(buttons)
            print(main_menu_interface)
    elif current_interface == "SETTINGS":
        if has_changed:
            buttons.clear()
            interface_group.empty()
            buttons.append(Button("Main menu", 100, 50, (0, 255, 0)))
            buttons.append(Button("Donut", 100, 150, (255, 255, 0)))
            interface_group.add(buttons)
            print(settings_interface)
    elif current_interface == "DONUT":
        print(donut_interface)
    elif current_interface == "LEVELS":
        left_button = "(L)" if current_level > 1 else "   "
        right_button = "(R)" if current_level < num_levels  else "   "
        print(" (0) -- основне меню")
        print(" (GO) -- запуск")
        print(levels_interface.format(levels[current_level - 1], left_button, right_button))
    elif current_interface == "GAME":
        fire_hero.update(keys[pygame.K_a], keys[pygame.K_d], keys[pygame.K_SPACE], platforms)
        water_hero.update(keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_UP], platforms)

        entities.draw(display)
    interface_group.draw(display)

def init(lvl):
    global fire_hero, water_hero, entities, platforms
    fire_hero = Player(img=ASSETS['fire'])
    water_hero = Player(img=ASSETS['water'])

    entities, platforms = create_level(lvl)

    entities.add(fire_hero)
    entities.add(water_hero)

main_menu_interface = """
    Вибери кнопку:
    1) рівні
    2) settings
    3) donut
    4) exit
"""

settings_interface = """
    Тут можна було настроїти опції, але програмістам не видали грошей на це. Зажали.
    
    0) Основне меню
    1) Закинути донат
    """

donut_interface = """
  Моя Bitcoin адреса: ....
  Чекаю.

  0) Основне меню
"""

num_levels = 9
levels = [ f"Левел {x}" for x in range(1, num_levels+1) ]

levels_interface = """
{1}  |     {0}     |  {2}
"""

current_level = 1

current_interface = ""

def handle_menu(keys, clicked_buttons):
    global current_interface, current_level
    print(clicked_buttons)
    button = clicked_buttons[0].name if clicked_buttons else None

    if current_interface == "":
        current_interface = "MAIN_MENU"
        return True
    
    if current_interface == "MAIN_MENU" and keys[pygame.K_4]:
        print("EXit")
        #sys.exit(0)
    elif  current_interface == "MAIN_MENU" and button == "Рівні":
        current_interface = "LEVELS"
        return True
    elif  current_interface == "MAIN_MENU" and button == "Settings":
        current_interface = "SETTINGS"
        return True
    elif  current_interface == "MAIN_MENU" and button == "Donut":
        current_interface = "DONUT" 
        return True

    elif  current_interface == "SETTINGS" and button == "Main menu":
        current_interface = "MAIN_MENU"
        return True
    elif  current_interface == "SETTINGS" and button == "Donut":
        current_interface = "DONUT"
        return True

    elif  current_interface == "DONUT" and keys[pygame.K_0]:                                
        current_interface = "MAIN_MENU"
        return True

    elif current_interface == "LEVELS" and keys[pygame.K_RETURN]:
        current_interface = "GAME"
        if current_level == 1:
            init(level1)
        elif current_level == 2:
            init(level2)
        else:
            print("no such level")
        return True
    elif current_interface == "LEVELS" and keys[pygame.K_0]:
        current_interface = "MAIN_MENU"
        return True
    elif current_interface == "LEVELS" and keys[pygame.K_r]:
        current_level += 1
        if current_level == 10:
            current_level -= 1 
        return True
    elif current_interface == "LEVELS" and keys[pygame.K_l]:
        if current_level == 1:
            print("куда пішов, а ну вперед!")
        elif 1 < current_level < 9:
            current_level -= 1
        elif current_level == 9:
            current_level -= 1
        return True
    return False
game()
