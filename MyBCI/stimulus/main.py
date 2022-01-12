import pygame
from pygame import Surface, Rect


def create(flag, a=5, b=5, w=250, h=250):  # 创建刺激源图像
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
]
A = IMAGES[0].get_width()


class FlickyManager:
    def __init__(self, scr):
        self.flickies = []
        self.screen = scr

    def addFlicky(self, f):
        self.flickies.append(f)

    def add(self, location, frames):
        w, h = self.screen.get_size()
        if location == 'left':
            x = 0
            y = h / 2 - A / 2
        elif location == 'right':
            x = w - A
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


pygame.init()
screen = pygame.display.set_mode([1920, 1080])  # 设置背景大小
pygame.display.set_caption("SSVEP")

done = False
clock = pygame.time.Clock()
flickymanager = FlickyManager(screen)

# 设置位置和刷新半周期
# flickymanager.add('left', 5)
# flickymanager.add('top', 6)
# flickymanager.add('right', 3)
# flickymanager.add('bottom', 7)
flickymanager.add('center', 5)

while not done:
    for event in pygame.event.get():
        if (event.type == pygame.KEYUP) or (event.type == pygame.KEYDOWN):
            if event.key == pygame.K_ESCAPE:
                done = True
        if event.type == pygame.QUIT:
            done = True
    screen.fill((0, 0, 0))
    clock.tick(150)
    flickymanager.process()
    flickymanager.draw()
    pygame.display.flip()

pygame.quit()
