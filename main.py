
import npgame
import pathlib

import levels
import objects
TEXTURES = pathlib.Path(__file__).parent / 'textures'

lvl = levels.WALLS[1:-1].split('\n')[::-1]
grid = len(lvl[0]), len(lvl)
game = npgame.Game(grid, scale=50, fps=2)
game.title('Br-Br-Br-Br-Br-Beakout!!!!!!!')
game.grid = grid

on = True
while on:

    game.objects = []
    game.score = 0
    game.lives = 20
    game.bricks = 0
    def call_reset_screen():
        screen = game.objects.append(objects.Reset_Screen(game, 1.2, game.grid[1] / 2))
        return screen


    for y, row in enumerate(lvl):
        for x, char in enumerate(row):
            if char == 'o':
                game.objects.append(objects.Brick(game, x, y))
                # game.add(objects.Brick, x, 6)
            if char == '#' or char =='s':
                game.objects.append(objects.Wall(game, x, y))
            if char == 'p':
                game.objects.append(objects.Paddle(game, x, y))
            if char == 'b':
                game.objects.append(objects.Ball(game, x, y))
            if char == '^':
                game.objects.append(objects.Death(game, x, y))
            if char == 's':
                game.objects.append(objects.Scoreboard(game, x, y))
            if (x, y) == (7, 0):  # TODO
                game.thewall = game.objects[-1]


    while game.running:
        # print('------------------')
        game.update()
        game.delta = 0.01
        if game.pressed('escape'):
            game.close()
            # game.running = False
            on = False
        if game.pressed('space'):
            game.objects.append(objects.Ball(game, grid[0] / 2, grid[1] / 2))
        if game.lives > 0 or game.bricks < 0:
            for obj in game.objects:
                obj.updated = False
            for obj in game.objects:
                obj.update()
                obj.updated = True
        else:
            call_reset_screen()
            game.objects.append(objects.Reset_Screen(game, x, y))
            if game.pressed('y'):
                game.running = False
                on = True
            if game.pressed('n'):
                game.running = False
                on = False

        game.draw(0, 0, *grid, image=TEXTURES / 'bg.png')
        for obj in sorted(game.objects, key=lambda obj: obj.z):
            obj.draw()


