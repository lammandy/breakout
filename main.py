
import npgame

import levels
import objects

lvl = levels.LEVEL[1:-1].split('\n')[::-1]
grid = len(lvl[0]), len(lvl)
game = npgame.Game(grid, scale=50)
game.grid = grid 
game.objects = []

for y, row in enumerate(lvl):
    for x, char in enumerate(row):
        if char == 'o':
            game.objects.append(objects.Brick(game, x, y))
        if char == '#':
            game.objects.append(objects.Wall(game, x, y))
        if char == 'p':
            game.objects.append(objects.Paddle(game, x, y))
        if char == 'b':
            game.objects.append(objects.Ball(game, x, y))
        if char == '^':
            game.objects.append(objects.Death(game, x, y))

while game.running:
    game.update()
    if game.pressed('escape'):
        game.running = False
    if game.pressed('space'):
        game.objects.append(objects.Ball(game, grid[0] / 2, grid[1] / 2))
    for obj in game.objects:
        obj.update()

    game.draw(0, 0, *grid, (0, 0, 0))
    for obj in sorted(game.objects, key=lambda obj: obj.z):
        obj.draw()