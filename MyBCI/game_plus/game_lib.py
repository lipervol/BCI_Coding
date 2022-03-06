import pygame
import random
from pygame import Surface, Rect

W, H, fps = 1920, 1080, 120
UPDATE_ENEMY_EVENT = pygame.USEREVENT
HERO_FIRE_EVENT = pygame.USEREVENT + 1


# 创建刺激源图像
def create(flag, a=5, b=5, w=250, h=250):
    k = w / a
    l = h / b
    surf = Surface((w, h))
    c = (0, 0, 0) if flag else (255, 255, 255)
    surf.fill(c)
    for i in range(0, a):
        for j in range(0, b):
            c = (255, 255, 255) if c == (0, 0, 0) else (0, 0, 0)
            r = Rect(k * i, l * j, k, l)
            surf.fill(c, r)
    return surf


IMAGES = [
    create(0),
    create(1)
]  # 定义图像
A = IMAGES[0].get_width()


# 控制图像闪烁
class FlickyManager:
    def __init__(self, scr):
        self.flickies = []
        self.screen = scr

    def addFlicky(self, f):
        self.flickies.append(f)

    def add(self, location, frames):
        w, h = self.screen.get_size()
        if location == 'left':
            x = A / 2
            y = h / 2 - A / 2
        elif location == 'right':
            x = w - A - A / 2
            y = h / 2 - A / 2
        elif location == 'top':
            y = 0
            x = w / 2 - A / 2
        elif location == 'bottom':
            y = h - A
            x = w / 2 - A / 2
        elif location == 'center':
            y = h / 2 - A / 2
            x = w / 2 - A / 2
        else:
            raise ValueError("location %s unknown" % location)
        f = Flicky(x, y, frames)
        self.flickies.append(f)

    def process(self):
        for f in self.flickies:
            f.process()

    def draw(self):
        for f in self.flickies:
            f.draw(self.screen)


# 每一个闪烁的定义
class Flicky(object):
    def __init__(self, x, y, frames=10, w=A, h=A):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.frames = frames
        self.clock = 0
        self.img_index = 0

    def process(self):
        self.clock = self.clock + 1
        if self.clock >= self.frames:
            self.clock = 0
            self.img_index = 0 if self.img_index == 1 else 1

    def draw(self, scr):
        scr.blit(IMAGES[self.img_index], (self.x, self.y))


# 玩家
class Hero(pygame.sprite.Sprite):
    def __init__(self, image_name, speed=0):
        super(Hero, self).__init__()
        self.image = pygame.transform.scale(pygame.image.load(image_name), (120, 95))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = W / 2 - self.image.get_size()[0] / 2, H - 2 * self.image.get_size()[1]
        self.bullets = pygame.sprite.Group()
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x < 250 + A / 2:
            self.rect.x = 250 + A / 2
        if self.rect.x > W - self.rect.width - 250 - A / 2:
            self.rect.x = W - self.rect.width - 250 - A / 2

    def fire(self):
        for i in range(0, 1, 2):
            bullet = Bullet("./bullet.png")
            bullet.rect.bottom = self.rect.y - i * 20
            bullet.rect.centerx = self.rect.centerx

            self.bullets.add(bullet)


# 敌人
class Enemy(pygame.sprite.Sprite):
    def __init__(self, image_name, speed=1):
        super(Enemy, self).__init__()
        self.image = pygame.transform.scale(pygame.image.load(image_name), (150, 120))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(int(A / 2 + 250), int(W - self.rect.width - 250 - A / 2))
        self.speed = speed
        self.status = 0
        self.break_idx = 0

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 2 * H / 3:
            self.rect.y = 0
            self.rect.x = random.randint(int(A / 2 + 250), int(W - self.rect.width - 250 - A / 2))

    def __del__(self):
        pass


# 子弹
class Bullet(pygame.sprite.Sprite):
    def __init__(self, image_name, speed=-2):
        super(Bullet, self).__init__()
        self.image = pygame.transform.scale(pygame.image.load(image_name), (30, 60))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, W - self.rect.width)
        self.rect.y = H / 2
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

    def __del__(self):
        pass


# 游戏
class Game(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((W, H))
        pygame.display.set_caption("SSVEP")
        self.clock = pygame.time.Clock()
        self.__create_sprites()
        self.flickymanager = FlickyManager(self.screen)
        self.flickymanager.add("left", 5)
        self.flickymanager.add("right", 4)
        self.font = pygame.font.SysFont("./font/cambriai.ttf", 60)
        self.text = self.font.render("score:0", True, (255,255,255))
        self.score = 0
        pygame.time.set_timer(UPDATE_ENEMY_EVENT, 10)
        pygame.time.set_timer(HERO_FIRE_EVENT, 240)

    def __create_sprites(self):
        self.hero = Hero("./hero.png")
        self.hero_group = pygame.sprite.Group()
        self.hero_group.add(self.hero)

        self.enemy = Enemy("./enemy.png")
        self.enemy_group = pygame.sprite.Group()
        self.enemy_group.add(self.enemy)

    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == UPDATE_ENEMY_EVENT and self.enemy.status == 0:
                self.enemy_group.update()
            if event.type == HERO_FIRE_EVENT:
                self.hero.fire()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_LEFT:
                    self.hero.speed = -2
                if event.key == pygame.K_RIGHT:
                    self.hero.speed = 2

    def __update_sprites(self):
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)
        self.enemy_group.draw(self.screen)
        self.flickymanager.process()
        self.flickymanager.draw()

    def __check_collide(self):
        hit_list = pygame.sprite.groupcollide(self.hero.bullets,self.enemy_group,True,False)
        if hit_list and self.enemy.status == 0:
            self.enemy.status = 1
            self.score += 1
            self.text = self.font.render("score:" + str(self.score), True, (255,255,255))
        if self.enemy.status == 1:
            if self.enemy.break_idx//4 < 9:
                self.enemy.image = pygame.transform.scale(pygame.image.load("./break/"+str(self.enemy.break_idx//4)+".png"), (150, 120))
                self.enemy.break_idx += 1
            else:
                self.enemy.status = 2
        if self.enemy.status == 2:
            self.enemy.kill()
            self.enemy = Enemy("./enemy.png")
            self.enemy_group.add(self.enemy)

    def start_game(self):
        pygame.init()
        while True:
            self.screen.fill((0, 0, 0))
            self.clock.tick_busy_loop(fps)
            self.__event_handler()
            self.__check_collide()
            self.__update_sprites()
            self.screen.blit(self.text, (A / 2, A / 2))
            pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.start_game()
