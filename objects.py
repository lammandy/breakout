import pathlib
import numpy as np
import physics 

TEXTURES = pathlib.Path(__file__).parent / 'textures'


class Object:
    
    def __init__(self, game, x, y, w=1, h=1, z=0, image=None, color=(1, 1, 1)):
        self.game = game
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.z = z
        self.image = image
        self.color = color

    def on_collision(self, obj):
        pass

    def update(self):
        pass

    def draw(self):
        if self.image:
            self.game.draw(self.x, self.y, self.w, self.h, image=TEXTURES / self.image)
        else:
            self.game.draw(self.x, self.y, self.w, self.h, color=self.color)



class Ball(Object):

    def __init__(self, game, x, y):
        super().__init__(game, x, y, w=0.8, h=0.8, z=1)
        self.speedx = -10 /2
        self.speedy = 12 /2

    def update(self):
        # print(self.x, self.y, self.speedx, self.speedy)
        
        prev_pos = self.x, self.y
        self.x += self.speedx * self.game.delta
        self.y += self.speedy * self.game.delta

        # self.speedy -= 100 * game.delta
        
        collision = None
        for obj in self.game.objects:
            if isinstance(obj, (Wall, Brick, Paddle, Death)):  #Wall, paddle, death
                collision = physics.collision(self, obj)
                if collision:
                    obj.collision = 1.0
                    break
        self.color = (0.3, 0.3, 0.3)
        if collision:
            obj.on_collision(self)
            collx, colly, collside = collision
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
            self.x = collx + self.speedx * max(0.01, self.game.delta * fraction_missing)
            self.y = colly + self.speedy * max(0.01, self.game.delta * fraction_missing)


class Brick(Object):

    def __init__(self, game, x, y):
        super().__init__(game, x + 0.1, y + 0.1, 0.8, 0.8, color=np.random.uniform(0, 1, 3))
    
    def on_collision(self, obj):
        if isinstance(obj, Ball):
            self.game.objects.remove(self)


class Wall(Object):

    def __init__(self, game, x, y):
        super().__init__(game, x, y, image='wall.png')


class Death(Object):

    def __init__(self, game, x, y):
        super().__init__(game, x, y, image='lava.png')
    
    def on_collision(self, obj):
        if isinstance(obj, Ball):
            self.game.objects.remove(obj)


class Paddle(Object):

    def __init__(self, game, x, y):
        super().__init__(game, x, y, w=2.5, h=0.7)
        self.speed = 10
    
    def on_collision(self, obj):
        pass

    def update(self):
        wall = next(obj for obj in self.game.objects if isinstance(obj, Wall))

        if (self.game.pressed('a') or self.game.pressed('j')):
            self.x -= self.speed * self.game.delta
        if self.game.pressed('d') or self.game.pressed('l'):
            self.x += self.speed * self.game.delta
        if self.x > self.game.grid[0] - self.w - wall.w:
            self.x = self.game.grid[0] - self.w - wall.w
        if self.x < wall.w:
            self.x = 0 + wall.w