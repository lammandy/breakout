import pathlib

import npgame
import numpy as np

import levels
import physics 

TEXTURES = pathlib.Path(__file__).parent / 'textures'


class Ball:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.z = 1
        self.w =  0.8
        self.h = 0.8
        self.speedx = -10
        self.speedy = 12
        self.color = (1, 1, 1)

    def update(self, game, objects):
        # print(self.x, self.y, self.speedx, self.speedy)
        prev_pos = self.x, self.y
        game.delta = 0.01
        self.x += self.speedx * game.delta
        self.y += self.speedy * game.delta

        # self.speedy -= 100 * game.delta
        
        collision = None
        for obj in objects:
            if isinstance(obj, (Wall, Brick, Paddle, Death)):  #Wall, paddle, death
                collision = physics.collision(self, obj)
                if collision:
                    obj.collision = 1.0
                    break
        self.color = (0.3, 0.3, 0.3)
        if collision:
            obj.on_collision(self, objects)
            collx, colly, collside = collision
            self.color = {
                'top': (1, 0, 0),
                'btm': (0, 1, 0),
                'lft': (0, 0, 1),
                'rgt': (1, 1, 1),
            }[collside]
            obj.color = self.color
            if collside == 'top' or collside == 'btm':
                self.speedy *= -1
            if collside == 'lft' or collside == 'rgt':
                self.speedx *= -1
            fraction_passed = (collx - prev_pos[0]) / (self.x - prev_pos[0])
            fraction_missing = 1 - fraction_passed
            # self.speedx *= 0.9
            # self.speedy *= 0.9
            # self.speedx *= 1.3
            # self.speedy *= 1.3
            self.x = collx + self.speedx * max(0.01, game.delta * fraction_missing)
            self.y = colly + self.speedy * max(0.01, game.delta * fraction_missing)



    def draw(self, game):
        game.draw(self.x, self.y, self.w, self.h, self.color)
        

class Brick:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.z = 0
        self.w = 1
        self.h = 1
        self.color = np.random.uniform(0, 1, 3)
    
    def on_collision(self, obj, objects):
        if isinstance(obj, Ball):
            objects.remove(self)

    def update(self, game, objects):
        pass

    def draw(self, game):
        game.draw(self.x, self.y, self.w, self.h, self.color)


class Wall:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.z = 0
        self.w = 1
        self.h = 1
        self.image = TEXTURES / 'wall.png'
        self.collision = 0
        self.color = (1, 1, 1)

    def on_collision(self, obj, objects):
        pass
    
    def update(self, game, objects):
        if self.collision > 0:
            self.collision -= game.delta

    def draw(self, game):        
        # if self.collision > 0:
        #     game.draw(self.x, self.y, self.w, self.h, color=self.color)
        # else:
        #     game.draw(self.x, self.y, self.w, self.h, image=self.image)

        game.draw(self.x, self.y, self.w, self.h, image=self.image)


class Death:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.z = 0
        self.w = 1
        self.h = 1
        self.image = TEXTURES / 'lava.png'
        self.color = (1, 1, 1)
    
    def on_collision(self, obj, objects):
        if isinstance(obj, Ball):
            objects.remove(obj)

    def update(self, game, objects):
        pass

    def draw(self, game):        
        game.draw(self.x, self.y, self.w, self.h, image=self.image)
    

class Paddle:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.z = 0
        self.w = 2.5
        self.h = 0.7
        self.speed = 10
        self.color = (1, 1, 1)
    
    def on_collision(self, obj, objects):
        pass

    def update(self, game, objects):
        wall = next(obj for obj in objects if isinstance(obj, Wall))

        if (game.pressed('a') or game.pressed('j')):
            self.x -= self.speed * game.delta
        if game.pressed('d') or game.pressed('l'):
            self.x += self.speed * game.delta
        if self.x > len(lvl[0]) - self.w - wall.w:
            self.x = len(lvl[0]) - self.w - wall.w
        if self.x < wall.w:
            self.x = 0 + wall.w

    def draw(self, game):
        game.draw(self.x, self.y, self.w, self.h, self.color)


objects = []

lvl = levels.LEVEL[1:-1].split('\n')[::-1]
grid = len(lvl[0]), len(lvl)
for y, row in enumerate(lvl):
    for x, char in enumerate(row):
        if char == 'o':
            objects.append(Brick(x, y))
        if char == '#':
            objects.append(Wall(x, y))
        if char == 'p':
            objects.append(Paddle(x, y))
        if char == 'b':
            objects.append(Ball(x, y))
        if char == '^':
            objects.append(Death(x, y))
objects = sorted(objects, key=lambda obj: obj.z)


game = npgame.Game(grid, scale=50)
while game.running:
    game.update()
    if game.pressed('escape'):
        game.running = False
    if game.pressed('space'):
        ball = Ball(grid[0] / 2, grid[1] / 2)
        objects.append(ball)
    for obj in objects:
        obj.update(game, objects)

    game.draw(0, 0, *grid, (0, 0, 0))
    for obj in objects:
        obj.draw(game)