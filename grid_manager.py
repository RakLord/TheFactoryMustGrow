import objects
from CONFIG import *


def new_game_grid():
    new_grid = []
    for row in range(0, GRID_HEIGHT):
        new_grid.append([])
        [new_grid[-1].append(tiles.empty_tile.EmptyTile(row, col, 0)) for col in range(0, GRID_WIDTH)]
    # print(f"Rows: {len(new_grid)}")
    # print(f"Cols: {len(new_grid[0])}")
    new_grid[8][0] = tiles.import_tile.ImportTile(8, 0, 1)
    return new_grid


def place_object(old_grid, place_pos, new_object, rotation):
    new_grid = old_grid
    place_row, place_col = place_pos
    if place_row <= GRID_HEIGHT:
        new_grid[place_row][place_col] = new_object(place_row, place_col, rotation)
