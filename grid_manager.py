import CONFIG
from CONFIG import *
import tiles
from tiles import *


def new_game_grid():
    new_grid = []
    for row in range(0, CONFIG.GRID_HEIGHT):
        new_grid.append([])
        [new_grid[-1].append(tiles.empty_tile.EmptyTile(row, col, 0)) for col in range(0, CONFIG.GRID_WIDTH)]
    # print(f"Rows: {len(new_grid)}")
    # print(f"Cols: {len(new_grid[0])}")
    new_grid[0][0] = tiles.import_tile.ImportTile(0, 0, 1)
    return new_grid


def place_object(old_grid, place_pos, new_object, rotation):
    new_grid = old_grid
    place_row, place_col = place_pos
    if place_row <= CONFIG.GRID_HEIGHT:
        new_grid[place_row][place_col] = new_object(place_row, place_col, rotation)


def locked_tiles(old_grid, unlock_level):
    new_grid = old_grid
    unlocked_tiles = []
    for row in range(0, unlock_level):
        for col in range(0, unlock_level):
            unlocked_tiles.append([col, row])

    for row in range(0, CONFIG.GRID_HEIGHT):
        for col in range(0, CONFIG.GRID_WIDTH):
            if [row, col] not in unlocked_tiles:
                place_object(old_grid, (row, col), tiles.locked_tile.LockedTile, 0)
            elif old_grid[row][col].type == "locked_tile":
                place_object(old_grid, (row, col), tiles.empty_tile.EmptyTile, 0)


