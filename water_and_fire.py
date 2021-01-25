import pygame
import random

width = 400
height = 300
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

            update(dt, keys)
            
            pygame.display.flip()
    except KeyboardInterrupt:
        return
    except:
        pygame.quit()
        raise

    print("Finish")
    pygame.quit()

p1 = pygame.Vector2(width / 2, height / 2)
v1 = pygame.Vector2(2, 3)

objects = []

play_sprite = pygame.image.load('./play.png')
fire_sprite = pygame.image.load('./Огонь2.0.png')
fire = pygame.transform.smoothscale(fire_sprite, (100, 100))

for i in range(10):
    p = pygame.Vector2(width / 2, height / 2)
    v = pygame.Vector2(random.random(), random.random())
    objects.append((p, v))

def update_points(p, v):
    p.x = p.x + v.x
    p.y = p.y + v.y
    
    if p.y > height:
        v.y = -v.y
    if p.x > width:
        v.x = -v.x
    if p.y < 0:
        v.y = -v.y
    if p.x < 0:
        v.x = -v.x    

def update(dt, keys):
    #print(dt)
    display.fill((0,0,0))
    if keys[pygame.K_a]:
        p1.x = p1.x - 10
    elif keys[pygame.K_d]:
        p1.x = p1.x + 10

    update_points(p1, v1)
    #pygame.draw.circle(display, (255, 0, 0), (int(p1.x), int(p1.y)), 20, 2)
    display.blit(fire, (p1.x, p1.y))
    
    
    for p, v in objects:
        update_points(p, v)
        pygame.draw.circle(display, (0, 255, 0), (int(p.x), int(p.y)), 20, 2)
        

game()
