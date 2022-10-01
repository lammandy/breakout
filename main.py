import pathlib

import npgame
import pygame

import levels
import objects
from objects import bounce, bounce2, TEXTURES, SOUNDS

pygame.init()
pygame.mixer.init()

# bounce = pygame.mixer.Sound(SOUNDS / 'bounce.wav')

def load_level(game, lvl_str):
    lvl = lvl_str[1:-1].split('\n')[::-1]
    grid = len(lvl[0]), len(lvl)

    game.resize(grid, scale=50)
    game.grid = grid
    game.lvl = lvl
    game.objects = []
    game.score = 0
    game.lives = 10
    game.bricks = 0

    for y, row in enumerate(lvl):
        for x, char in enumerate(row):
            if char == 'o':
                game.objects.append(objects.Brick(game, x, y))
            if char == '#' or char =='s':
                wall = objects.Wall(game, x, y)
                wall.has_btm = (0 <= y - 1) and (lvl[y - 1][x] != '#')
                wall.has_top = (y + 1 < game.grid[1]) and (lvl[y + 1][x] != '#')
                wall.has_lft = (0 <= x - 1) and (lvl[y][x - 1] != '#')
                wall.has_rgt = (x + 1 < game.grid[0]) and (lvl[y][x + 1] != '#')
                game.objects.append(wall)
            if char == 'p':
                game.objects.append(objects.Paddle(game, x, y))
            if char == 'b':
                game.objects.append(objects.Ball(game, x, y))
            if char == '^':
                game.objects.append(objects.Death(game, x, y))
            if char == 's':
                game.objects.append(objects.Scoreboard(game, x, y))
            if char == '1':
                game.objects.append(objects.Text(game, x, y, 'start'))
            if char == '2':
                game.objects.append(objects.Text(game, x, y, 'choose level'))
            if char == '3':
                game.objects.append(objects.Text(game, x, y, 'quit'))                  
            if char == 'w':
                game.objects.append(objects.Wormhole(game, x, y))

def start_up_screen(pos, timer):
    if timer <= 0 and (game.pressed('w') or game.pressed('i')):
        pygame.mixer.Sound.play(bounce2)
        timer = 0.2
        if pos < 5:
            pos += 1
        else:
            pos = 5
    if timer <= 0 and (game.pressed('s') or game.pressed('k')):
        pygame.mixer.Sound.play(bounce2)
        timer = 0.2
        if pos > 3:
            pos -= 1
        else:
            pos = 3
    cursor = game.draw(4, pos, 0.45, 0.45, image= TEXTURES /'ball.png')
    return pos, timer

def run_game(game, level):
    reset_screen = None
    pos = 4
    timer = 0.2
    while game.running:
        if timer > 0:
            timer -= game.delta
        game.update()
        if level == levels.START_UP:
            pos, timer = start_up_screen(pos, timer)
            if game.pressed('return') and pos == 3:
                pygame.mixer.Sound.play(bounce)
                return False            
            if game.pressed('return') and pos == 4:
                pygame.mixer.Sound.play(bounce)
                return True, levels.CHOOSE_LVL
            if game.pressed('return') and pos == 5:
                pygame.mixer.Sound.play(bounce)
                return True, levels.SECRET_LEVEL
        # game.delta = 0.01
        if game.pressed('escape'):
            return False
        if game.lives > 0 and game.bricks > 0:
            if game.pressed('space'):
                game.objects.append(objects.Ball(game, game.grid[0] / 2, game.grid[1] / 2))
            for obj in game.objects:
                obj.update()
        non_levels = levels.START_UP, levels.CHOOSE_LVL
        if game.lives <= 0 or (game.bricks <= 0 and not (level == levels.START_UP or level == levels.CHOOSE_LVL)) :
            if not reset_screen:
                reset_screen = objects.Reset_Screen(game, 1.2, game.grid[1] / 2)
                game.objects.append(reset_screen)
            if game.pressed('y'):
                return True, levels.LEVEL
            if game.pressed('n'):
                return True, levels.START_UP
        for obj in sorted(game.objects, key=lambda obj: obj.z):
            obj.draw()
    return False


game = npgame.Game((10, 10), scale=50, fps=60)
game.title('Br-Br-Br-Br-Br-Beakout!!!!!!!')
level = levels.START_UP
while True:
    load_level(game, level)
    again, level = run_game(game, level)
    if not again:
        print('Goodbye :)')
        break
