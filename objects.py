import pygame
from msilib.schema import Font
import pathlib
import numpy as np
import physics 
import random


TEXTURES = pathlib.Path(__file__).parent / 'textures'
SOUNDS = pathlib.Path(__file__).parent / 'sounds'

pygame.init()
pygame.mixer.init()

bounce = pygame.mixer.Sound(SOUNDS / 'bounce.wav')
bounce2 = pygame.mixer.Sound(SOUNDS / 'bounce2.wav')
bounce3 = pygame.mixer.Sound(SOUNDS / 'bounce3.wav')
death = pygame.mixer.Sound(SOUNDS / 'death.wav')
final_death = pygame.mixer.Sound(SOUNDS / 'final_death.wav')
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
        self.updated = False
        self.highlight = 0
        self.has_top = True
        self.has_rgt = True
        self.has_btm = True
        self.has_lft = True

    def on_collision(self, obj, collside):
        self.timer = 0.5
        self.collside = collside

    def update(self):
        if self.timer > 0:
            self.timer -= self.game.delta
        if self.highlight > 0:
            self.highlight -= self.game.delta

    def draw(self):
        if self.image:
            self.game.draw(self.x, self.y, self.w, self.h, image=TEXTURES / self.image)
        else:
            self.game.draw(self.x, self.y, self.w, self.h, color=self.color)
        self.draw_higlight()

    def draw_higlight(self):
        return  # TODO
        if self.timer > 0:
            if self.collside == 'lft':
                self.game.draw(self.x, self.y, .1, self.h, color=(1, 1, 0))
            if self.collside == 'rgt':
                self.game.draw(self.x + self.w - .1, self.y, .1, self.h, color=(1, .5, 0)) # orange
            if self.collside == 'top':
                self.game.draw(self.x, self.y + self.h - .1, self.w, .1, color=(0.5, 1, 0))
            if self.collside == 'btm':
                self.game.draw(self.x, self.y, self.w, .1, color=(1, 1, 0.5))
        if self.highlight > 0:
            self.game.draw(self.x, self.y, self.w, self.h, color=(1, 0, 0, 0.5))

# TODO create choose level, quit -> make cursor movable
# TODO create choose level screen -> make highlight of object movable

class Text(Object):
    def __init__(self, game, x, y, msg_str):
        super().__init__(game, x, y, z=1)
        self.msg_str = msg_str
    def update(self):
        pass
    def draw(self):
        self.game.text(self.x, self.y, message=self.msg_str, font='slkscr.ttf', color=(1, 1, 1), size=.7)

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
        self.message = "'n' to choose new level, 'esc' to quit"
        message_width = len(self.message) * 0.35
        self.margin = (game.grid[0] - message_width) /2
        self.x = self.margin
        self.y = game.grid[1] / 2
        
    def update(self):
        pass
    def draw(self):
        self.game.text(self.x, self.y, message=f"Final Score: {str(self.game.score)} Press 'y' to continue", font='slkscr.ttf', color=(1, 1, 1), size=.6)
        self.game.text(self.x, self.y - 0.7, message=self.message, font='slkscr.ttf', color=(1, 1, 1), size=.6)


class Ball(Object):
    
    def __init__(self, game, x, y):
        super().__init__(game, x, y, w=0.5, h=0.5, z=2, image='ball.png')
        self.speedx = -2.4
        self.speedy = -4.249
        self.shadow1 = [0, 0, 0]
        self.shadow2 = [0, 0, 0]
        self.shadow3 = [0, 0, 0]

    def on_collision(self, obj, side):
        # super().on_collision(obj, side)
        if isinstance(obj, Paddle):
            pygame.mixer.Sound.play(bounce)
            self.speedx += 0.6 * self.speedx
            self.speedy += 0.6 * self.speedy

    def update(self):
        super().update()
        self.shadow1[0] -= self.game.delta
        self.shadow2[0] -= self.game.delta
        self.shadow3[0] -= self.game.delta

        # print('BEFORE MOVING', physics.intersects(self, self.game.thewall))

        speed = np.sqrt(self.speedx ** 2 + self.speedy ** 2)
        if speed > 5:
            self.speedx = self.speedx / (speed / 5)
            self.speedy = self.speedy / (speed / 5)

        self.shadow2 = [0.0001, self.x, self.y] # grey
        self.shadow3 = [0.0001, self.x + self.speedx * self.game.delta, self.y + self.speedy * self.game.delta] # green

        # time_left = self.game.delta
        # while time_left > 0.001:
        #     duration = time_left
        #     time_left, _ = physics.move_until_collision(
        #         self, self.game.objects, (Wall, Brick, Paddle, Death), duration)
        physics.move_until_collision(
                 self, self.game.objects, (Wall, Brick, Paddle, Death, Wormhole), self.game.delta)

        # for obj in self.game.objects:
        #     if obj is self:
        #         continue
        #     if physics.intersects(self, obj):
        #         if isinstance(obj, Ball):
        #             continue
        #         print('Ball intersects with', obj, 'at', obj.x, obj.y)
        #         obj.highlight = 1
            

        # print(self.x, self.y, self.speedx, self.speedy)


        # collision = None
        # dist = None
        # for obj in self.game.objects:
        #     if isinstance(obj, (Wall, Brick, Paddle, Death)):
        #         current = physics.collision(self, obj, self.game.delta)
        #         if not current:
        #             continue
        #         # current = list(current)
        #         new_dist = np.sqrt((obj.x + obj.w/2 - self.x - self.w/2) ** 2 + (obj.y + obj.h/2 - self.y - self.h/2) ** 2) # how far it went in from static mid point to want
 
        #         moved = np.sqrt((current[0] - self.x) ** 2 + (current[1] - self.y) ** 2) # dist from after moved to pre_pos
        #         total = np.sqrt(self.speedx ** 2 + self.speedy ** 2) # velocity
        #         time_moved = self.game.delta * moved / total 
        #         current += (time_moved, obj)
        #         if not dist or dist > new_dist:
        #             dist = new_dist
        #             collision = current
        #         # elif current[3] < collision[3]:
        #             # x_farther, y_farther = collision[:2]
        #             # x_closer, y_closer = current[:2]
        #             # d_closer = np.sqrt((x_closer - self.x) ** 2 + (y_closer - self.y) ** 2)
        #             # d_farther = np.sqrt((x_farther - self.x) ** 2 + (y_farther - self.y) ** 2)
        #             # assert d_closer < d_farther, (collision, current)
        #             # collision = current + [obj]
        #         # if current and (not collision or current[3] < collision[3]):
        #         #     collision = current + (obj,)

        # if collision:
        #     # print('COOOOOOOOLLISSSSION!', '(with THE wall?', obj is self.game.thewall, ')')
        #     self.x, self.y, coll_side, time_moved, obj = collision
        #     self.shadow1 = [1, self.x, self.y]
        #     obj.on_collision(self, coll_side)
        #     if coll_side == 'top' or coll_side == 'btm':
        #         self.speedy *= -1
        #     if coll_side == 'lft' or coll_side == 'rgt':
        #         self.speedx *= -1
        #     self.x += self.speedx * (self.game.delta - time_moved)
        #     self.y += self.speedy * (self.game.delta - time_moved)
        # else:
        #     # print('GOOD TO GO ^_^')
        #     # assert not physics.intersects(self, self.game.thewall)
        #     self.x += self.speedx * self.game.delta
        #     self.y += self.speedy * self.game.delta

        # print('AFTER MOVING', physics.intersects(self, self.game.thewall))
        # print(f'{self.x}, {self.y}, {self.speedx}, {self.speedy}')
    
    # def draw(self):
    #     if self.shadow1[0] > 0:
    #         self.game.draw(self.shadow1[1], self.shadow1[2], self.w, self.h, (1, .2, .2, .5))
    #     if self.shadow2[0] > 0:
    #         self.game.draw(self.shadow2[1], self.shadow2[2], self.w, self.h, (.7, .7, .7, .5))
    #     if self.shadow3[0] > 0:
    #         self.game.draw(self.shadow3[1], self.shadow3[2], self.w, self.h, (.2, 1, .2, .5))
    #     super().draw()

class Brick(Object):
    def __init__(self, game, x, y, size=0.5):
        x += (1 - size) / 2 + np.random.uniform(-0.05, 0.05)
        y += (1 - size) / 2 + np.random.uniform(-0.05, 0.05)
        super().__init__(game, x, y, size, size, color=np.random.uniform(0, 1, 3))
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
        # self.has_btm = False

    def on_collision(self, obj, collside):
        super().on_collision(obj, collside)
        if isinstance(obj, Ball):
            pygame.mixer.Sound.play(bounce3)

    def draw(self):
        super().draw()
        if self.has_lft:
            self.game.draw(self.x, self.y, .1, self.h, color=(0, 0, 1))
        if self.has_rgt:
            self.game.draw(self.x + self.w - .1, self.y, .1, self.h, color=(1, .5, 0)) # orange
        if self.has_top:
            self.game.draw(self.x, self.y + self.h - .1, self.w, .1, color=(0.5, 1, 0))
        if self.has_btm:
            self.game.draw(self.x, self.y, self.w, .1, color=(1, 1, 0.5))

        
class Death(Object):

    def __init__(self, game, x, y):
        super().__init__(game, x, y, image='lava.png')
    
    def on_collision(self, obj, collside):
        super().on_collision(obj, collside)
        if isinstance(obj, Ball):
            if obj in self.game.objects:
                self.game.objects.remove(obj)
            self.game.lives -= 1
            pygame.mixer.Sound.play(death)
        if self.game.lives != 0:
            # check if x, y = ' ', add ball
            num = random.choice(range(1, self.game.grid[0])) #grid row where it is okay for ball to generate wherever 
            self.game.objects.append(Ball(self.game, num, 5))
        if self.game.lives == 0:
            pygame.mixer.fadeout(5)
            pygame.mixer.Sound.play(final_death)


class Paddle(Object):

    def __init__(self, game, x, y):
        super().__init__(game, x + 0.01, y + 0.01, w=2.5, h=0.7, z=1, image='rug.png')
        self.speedx = 0
        self.speedy = 0
        self.color = (.8, .8, .8)

    def on_collision(self, obj, side):
        super().on_collision(obj, side)
        if isinstance(obj, Ball):
            pygame.mixer.Sound.play(bounce)
            obj.speedx += 0.3 * self.speedx
            obj.speedy += 0.3 * self.speedy

    def update(self):
        super().update()
        self.speedx = 0
        self.speedy = 0
        if (self.game.pressed('a') or self.game.pressed('j')):
            self.speedx = -7
        if (self.game.pressed('d') or self.game.pressed('l')):
            self.speedx = 7
        if (self.game.pressed('s') or self.game.pressed('k')):
            self.speedy = -7
        if (self.game.pressed('w') or self.game.pressed('i')):
            self.speedy = 7

        time_left, obj, side = physics.move_until_collision(
            self, self.game.objects, (Wall, Brick, Ball), self.game.delta)
        # if isinstance(obj, Ball):
        #     if side in ('lft', 'rgt'):
        #         obj.speedx *= -1
        #     if side in ('top', 'btm'):
        #         obj.speedy *= -1
        #     obj.speedx += 0.3 * self.speedx
        #     obj.speedy += 0.3 * self.speedy
        # if isinstance(obj, Ball):
        #     physics.move_until_collision(
        #         obj, self.game.objects, (Object,),
        #         self.game.delta - time_left)

        # for obj in self.game.objects:
        #     if obj is self:
        #         continue
        #     if physics.intersects(self, obj):
        #         print('Paddle intersects with', obj, 'at', obj.x, obj.y)
        #         obj.highlight = 1

        # for obj in self.game.objects:
        #     if isinstance(obj, (Ball, Wall, Brick)):
        #         if physics.intersects(self, obj):
        #             print(f'intersecting w/ {obj}')
        # self.speedx = 0
        # self.speedy = 0

    # def draw(self):
    #     self.game.draw(self.x, self.y, self.w, self.h, color=self.color)
    #     self.draw_higlight()


class Wormhole(Object):

    def __init__(self, game, x, y):
        super().__init__(game, x, y, color=(0, 1, 1))

    def on_collision(self, obj, collside):
        super().on_collision(obj, collside)
        if isinstance(obj, Ball):
            obj.x = 9
            obj.y = 5
            obj.speedx *= 0.5
            obj.speedy *= 0.5
            
# class Thumbnail(Object):

#     lvl = lvl_str[1:-1].split('\n')[::-1]