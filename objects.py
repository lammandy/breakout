import pygame
from msilib.schema import Font
import pathlib
import numpy as np
import physics 

TEXTURES = pathlib.Path(__file__).parent / 'textures'
SOUNDS = pathlib.Path(__file__).parent / 'sounds'

pygame.init()
pygame.mixer.init()

bounce = pygame.mixer.Sound(SOUNDS / 'bounce.wav')
bounce2 = pygame.mixer.Sound(SOUNDS / 'bounce2.wav')
bounce3 = pygame.mixer.Sound(SOUNDS / 'bounce3.wav')
death = pygame.mixer.Sound(SOUNDS / 'death.wav')
music = pygame.mixer.music.load(SOUNDS / 'arabian.wav')
pygame.mixer.music.play(-1)

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
        self.timer = 0
        self.collside = None

    def on_collision(self, obj, collside):
        self.timer = 0.5
        self.collside = collside

    def update(self):
        if self.timer > 0:
            self.timer -= self.game.delta

    def draw(self):
        if self.image:
            self.game.draw(self.x, self.y, self.w, self.h, image=TEXTURES / self.image)
        else:
            self.game.draw(self.x, self.y, self.w, self.h, color=self.color)
        self.draw_higlight()

    def draw_higlight(self):
        if self.timer > 0:
            if self.collside == 'lft':
                self.game.draw(self.x, self.y, .1, self.h, color=(1, 1, 0))
            if self.collside == 'rgt':
                self.game.draw(self.x + self.w - .1, self.y, .1, self.h, color=(1, .5, 0)) # orange
            if self.collside == 'top':
                self.game.draw(self.x, self.y + self.h - .1, self.w, .1, color=(0.5, 1, 0))
            if self.collside == 'btm':
                self.game.draw(self.x, self.y, self.w, .1, color=(1, 1, 0.5))


class Scoreboard(Object):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, z=1)
        self.y += .25
    def update(self):
        pass
    def draw(self):
        self.game.text(self.x, self.y, message='score: ' + str(self.game.score) + '       lives: ' + str(self.game.lives), font='slkscr.ttf', color=(1, 1, 1), size=.7)


class Reset_Screen(Object):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, z=1)
        self.x = 1.2 
        self.y = game.grid[1] / 2
    def update(self):
        pass
    def draw(self):
        self.game.text(self.x, self.y, message=f"Final Score: {str(self.game.score)} Press 'y' to continue or 'n' to quit", font='slkscr.ttf', color=(1, 1, 1), size=.6)


class Ball(Object):
    
    def __init__(self, game, x, y):
        super().__init__(game, x, y, w=0.5, h=0.5, z=2)
        # super().__init__(game, x= 2.6, y=1.95, w=0.5, h=0.5, z=2) # for Walls troubleshoot
        self.speedx = 2.0
        self.speedy = -1.5
        self.shadow1 = [0, 0, 0]
        self.shadow2 = [0, 0, 0]
        self.shadow3 = [0, 0, 0]

    def update(self):
        super().update()
        self.shadow1[0] -= self.game.delta
        self.shadow2[0] -= self.game.delta
        self.shadow3[0] -= self.game.delta

        print('BEFORE MOVING', physics.intersects(self, self.game.thewall))

        speed = np.sqrt(self.speedx ** 2 + self.speedy ** 2)
        if speed > 5:
            self.speedx = self.speedx / (speed / 5)
            self.speedy = self.speedy / (speed / 5)

        self.shadow2 = [0.0001, self.x, self.y]
        self.shadow3 = [0.0001, self.x + self.speedx * self.game.delta, self.y + self.speedy * self.game.delta]

        collision = None
        dist = None
        for obj in self.game.objects:
            if isinstance(obj, (Wall, Brick, Paddle, Death)):
                current = physics.collision(self, obj, self.game.delta)
                if not current:
                    continue
                # current = list(current)
                new_dist = np.sqrt((obj.x + obj.w/2 - self.x - self.w/2) ** 2 + (obj.y + obj.h/2 - self.y - self.h/2) ** 2)
                moved = np.sqrt((current[0] - self.x) ** 2 + (current[1] - self.y) ** 2)
                total = np.sqrt(self.speedx ** 2 + self.speedy ** 2)
                time_moved = self.game.delta * moved / total
                current += (time_moved, obj)
                if not dist or dist > new_dist:
                    dist = new_dist
                    collision = current
                # elif current[3] < collision[3]:
                    # x_farther, y_farther = collision[:2]
                    # x_closer, y_closer = current[:2]
                    # d_closer = np.sqrt((x_closer - self.x) ** 2 + (y_closer - self.y) ** 2)
                    # d_farther = np.sqrt((x_farther - self.x) ** 2 + (y_farther - self.y) ** 2)
                    # assert d_closer < d_farther, (collision, current)
                    # collision = current + [obj]
                # if current and (not collision or current[3] < collision[3]):
                #     collision = current + (obj,)

        if collision:
            # print('COOOOOOOOLLISSSSION!', '(with THE wall?', obj is self.game.thewall, ')')
            self.x, self.y, coll_side, time_moved, obj = collision
            self.shadow1 = [1, self.x, self.y]
            obj.on_collision(self, coll_side)
            if coll_side == 'top' or coll_side == 'btm':
                self.speedy *= -1
            if coll_side == 'lft' or coll_side == 'rgt':
                self.speedx *= -1
            self.x += self.speedx * (self.game.delta - time_moved)
            self.y += self.speedy * (self.game.delta - time_moved)
        else:
            # print('GOOD TO GO ^_^')
            # assert not physics.intersects(self, self.game.thewall)
            self.x += self.speedx * self.game.delta
            self.y += self.speedy * self.game.delta

        print('AFTER MOVING', physics.intersects(self, self.game.thewall))
        
        print(f'{self.x}, {self.y}, {self.speedx}, {self.speedy}')
    
    def draw(self):
        if self.shadow1[0] > 0:
            self.game.draw(self.shadow1[1], self.shadow1[2], self.w, self.h, (1, .2, .2, .5))
        if self.shadow2[0] > 0:
            self.game.draw(self.shadow2[1], self.shadow2[2], self.w, self.h, (.7, .7, .7, .5))
        if self.shadow3[0] > 0:
            self.game.draw(self.shadow3[1], self.shadow3[2], self.w, self.h, (.2, 1, .2, .5))
        super().draw()


class Brick(Object):
    def __init__(self, game, x, y):
        super().__init__(game, x + 0.1, y + 0.1, 0.8, 0.8, color=np.random.uniform(0, 1, 3))
        game.bricks += 1
    def on_collision(self, obj, collside):
        super().on_collision(obj, collside)
        if isinstance(obj, Ball):
            self.game.objects.remove(self)
            self.game.score += 10
            pygame.mixer.Sound.play(bounce2)


class Wall(Object):

    def __init__(self, game, x, y):
        super().__init__(game, x, y, image='wall.png')

    def on_collision(self, obj, collside):
        super().on_collision(obj, collside)
        if isinstance(obj, Ball):
            pygame.mixer.Sound.play(bounce3)

    def draw(self):
        super().draw()
        if self is self.game.thewall:
            self.game.draw(self.x, self.y, 1, 1, (1, 1, 1, 0.2))

        
class Death(Object):

    def __init__(self, game, x, y):
        super().__init__(game, x, y, image='lava.png')
    
    def on_collision(self, obj, collside):
        super().on_collision(obj, collside)
        if isinstance(obj, Ball):
            self.game.objects.remove(obj)
            self.game.lives -= 1
        if self.game.lives != 0:
            self.game.objects.append(Ball(self.game, 5, 5))
        if self.game.lives == 0:
            pygame.mixer.fadeout(5)
            pygame.mixer.Sound.play(death)


class Paddle(Object):

    def __init__(self, game, x, y):
        super().__init__(game, x + 0.01, y + 0.01, w=2.5, h=0.7, z=1)
        self.speedx = 0
        self.speedy = 0
        self.pausedx = 0
        self.pausedy = 0
        self.highlight = 0
        self.collside = ''
        self.color = (.8, .8, .8)

    def on_collision(self, obj, collside):
        super().on_collision(obj, collside)
        if isinstance(obj, Ball):
            pygame.mixer.Sound.play(bounce)
            self.highlight = 0.5
            self.collside = collside

            collision = physics.collision(obj, self, self.game.delta)
            if collision:
                _, _, side = collision
                if side == 'top' or side == 'btm':
                    self.pausedy = 0.1
                    # obj.speedx += 0.3 * self.speedx
                if side == 'lft' or side == 'rgt':
                    self.pausedx = 0.1
                    # obj.speedy += 0.3 * self.speedy
        obj.speedx += 0.3 * self.speedx
        obj.speedy += 0.3 * self.speedy

    def update(self):
        super().update()
        self.speedx = 0
        self.speedy = 0
        if (self.game.pressed('a') or self.game.pressed('j')):
            self.speedx = -10
        if (self.game.pressed('d') or self.game.pressed('l')):
            self.speedx = 10
        if (self.game.pressed('s') or self.game.pressed('k')):
            self.speedy = -10
        if (self.game.pressed('w') or self.game.pressed('i')):
            self.speedy = 10

        if self.pausedx > 0:
            self.speedx = 0
            self.pausedx -= self.game.delta
        if self.pausedy > 0:
            self.speedy = 0
            self.pausedy -= self.game.delta
        
        self.x += self.speedx * self.game.delta
        self.y += self.speedy * self.game.delta

        collision = None
        for obj in self.game.objects:
            if isinstance(obj, (Wall)): 
                collision = physics.collision(self, obj, self.game.delta)
                if collision:
                    break
        # highlight            
        if self.highlight > 0:
            self.highlight -= self.game.delta

        if collision:
            self.x, self.y, coll_side = collision
            obj.on_collision(self, coll_side)    
    
    def draw(self):
        self.game.draw(self.x, self.y, self.w, self.h, color=self.color)
        self.draw_higlight()