import numpy as np
from Board import Grid
from IA import IntelligentAgent
import random
import time

start = time.time()
grid = Grid()
IA = IntelligentAgent()
grid.print()

while True:
    available_cells = grid.getAvailableCells()
    if len(available_cells) > 0:
        new_tile = random.choice(available_cells), np.random.choice([2, 4], p=[.8, .2])
        grid.insertTile(new_tile[0], new_tile[1])
        print("Game:")
        grid.print()
    else:
        break

    move = IA.get_move(grid.clone())

    if move is not None and 0 <= move < 4 and grid.canMove([move]):
        grid.move(move)
        print("AI:")
        grid.print()
    else:
        break

print("Game Over")
print("Highest Tile: ", grid.getMaxTile())
print("Game Time: ", round((time.time()-start), 2), "s")




