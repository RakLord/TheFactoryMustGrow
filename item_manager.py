import objects
from CONFIG import *
import CONFIG
import pygame
from pygame.locals import *

active_items = []


class Item(object):
    def __init__(self, display, ore_type, grid_x, grid_y, rotation, value):
        self.display = display
        self.type = "ore"
        self.ore_type = ore_type
        self.base_value = value
        self.value = self.base_value
        self.x = grid_x
        self.y = grid_y
        self.rect = pygame.Rect((self.y + CONFIG.ITEM_COLLIDER_HITBOX, self.x + CONFIG.ITEM_COLLIDER_HITBOX), (CONFIG.TILE_SIZE - (CONFIG.ITEM_COLLIDER_HITBOX * 2), CONFIG.TILE_SIZE - (CONFIG.ITEM_COLLIDER_HITBOX * 2)))
        self.direction = rotation
        self.moving = True
        self.tiles_used = []

        if self.direction == 0:
            self.vector = [1, 0]
        elif self.direction == 1:
            self.vector = [0, 1]
        elif self.direction == 2:
            self.vector = [-1][0]
        else:
            self.vector = [0][-1]

    def draw(self, display):
        self.display.blit(CONFIG.IMAGES[self.ore_type], (self.rect.x - self.rect.width, self.rect.y - self.rect.height - 4))
        pygame.draw.rect(display, (245, 250, 200), self.rect, 1)

    def tick(self, **kwargs):

        if self.direction == 0 and self.moving:
            self.vector = [0, 1]
        elif self.direction == 1 and self.moving:
            self.vector = [1, 0]
        elif self.direction == 2 and self.moving:
            self.vector = [0, -1]
        elif self.direction == 3 and self.moving:
            self.vector = [-1, 0]
        else:
            self.vector = [0, 0]
        current_tile = kwargs.get("current_tile")
        buildings_grid = kwargs.get("building_grid")
        for index1, row in enumerate(buildings_grid):
            for index2, tile in enumerate(row):
                if pygame.Rect.colliderect(tile.rect, self.rect):  # Returning current tile is breaking it ugh fix later fatty
                    current_tile = type(tile).__name__
                    if type(tile).__name__ == "BeltTile":
                        self.direction = tile.rotation

                    elif type(tile).__name__ == "EmptyTile":
                        return "dead", current_tile

                    elif type(tile).__name__ == "ExportTile":
                        return "export", current_tile

                    elif type(tile).__name__ == "SimpleUpgraderTile":
                        if tile not in self.tiles_used:
                            self.value = tile.func(self.value)
                            self.tiles_used.append(tile)
                            return False, current_tile

        self.rect.x += kwargs.get("belt_speed_value") * self.vector[0]
        self.rect.y += kwargs.get("belt_speed_value") * self.vector[1]
        self.x = self.rect.x
        self.y = self.rect.y


def spawn_ore(display, rotation, spawn_tile_grid_y, spawn_tile_grid_x):
    print(f"New Item:\n > Type: iron_ore\n > Grid_X: {spawn_tile_grid_x} | Grid_Y: {spawn_tile_grid_y}")
    active_items.append(Item(display, "iron_ore", spawn_tile_grid_y * CONFIG.TILE_SIZE, spawn_tile_grid_x * CONFIG.TILE_SIZE, rotation, 1))
