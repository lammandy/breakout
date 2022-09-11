import pathlib

import npgame

import levels
import objects


def load_level(game, lvl_str):
    lvl = lvl_str[1:-1].split('\n')[::-1]
    grid = len(lvl[0]), len(lvl)

    game.resize(grid, scale=50)
    game.grid = grid
    game.objects = []
    game.score = 0
    game.lives = 20
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


def run_game(game):
    reset_screen = None
    while game.running:
        # print('------------------')
        game.update()
        # game.delta = 0.01
        if game.pressed('escape'):
            return False
        if game.lives > 0 and game.bricks > 0:
            if game.pressed('space'):
                game.objects.append(objects.Ball(game, game.grid[0] / 2, game.grid[1] / 2))
            for obj in game.objects:
                obj.update()
        else:
            if not reset_screen:
                reset_screen = objects.Reset_Screen(game, 1.2, game.grid[1] / 2)
                game.objects.append(reset_screen)
            if game.pressed('y'):
                return True
            if game.pressed('n'):
                return False
        for obj in sorted(game.objects, key=lambda obj: obj.z):
            obj.draw()
    return False


game = npgame.Game((10, 10), scale=50, fps=60)
game.title('Br-Br-Br-Br-Br-Beakout!!!!!!!')
while True:
    load_level(game, levels.SECRET_LEVEL)
    again = run_game(game)
    if not again:
        print('Goodbye :)')
        break
