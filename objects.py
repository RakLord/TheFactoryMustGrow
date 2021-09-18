import CONFIG
import pygame
import item_manager as im
from pygame.locals import *
import math


def calc_dist(obj_1, obj_2):  # Calculates the vector between 2 objects
    dist = math.hypot(obj_1[0] - obj_2[0], obj_1[1] - obj_2[1])
    return dist


def draw(building_type, display, index1, index2, rotation):
    if rotation == 0:
        display.blit(building_type, (index2 * CONFIG.TILE_SIZE, index1 * CONFIG.TILE_SIZE))
    if rotation == 1:
        display.blit(pygame.transform.rotate(building_type, 90), (index2 * CONFIG.TILE_SIZE, index1 * CONFIG.TILE_SIZE))
    if rotation == 2:
        display.blit(pygame.transform.rotate(building_type, 180), (index2 * CONFIG.TILE_SIZE, index1 * CONFIG.TILE_SIZE))
    if rotation == 3:
        display.blit(pygame.transform.rotate(building_type, 270), (index2 * CONFIG.TILE_SIZE, index1 * CONFIG.TILE_SIZE))


class EmptyTile(object):
    def __init__(self, grid_col, grid_row, rotation):  # Col/row passed inb backwards cba to fix rn lmao
        self.x = grid_col * CONFIG.TILE_SIZE
        self.y = grid_row * CONFIG.TILE_SIZE
        self.rect = pygame.Rect((self.y + CONFIG.ITEM_COLLIDER_HITBOX, self.x + CONFIG.ITEM_COLLIDER_HITBOX), (CONFIG.TILE_SIZE - (CONFIG.ITEM_COLLIDER_HITBOX * 2), CONFIG.TILE_SIZE - (CONFIG.ITEM_COLLIDER_HITBOX * 2)))
        self.rotation = rotation
        self.type = "empty_tile"

    def draw(self, display, index1, index2):
        draw(CONFIG.IMAGES[self.type], display, index1, index2, self.rotation)
        # pygame.draw.rect(display, (40, 40, 190), self.rect, 1)


class BeltTile(object):
    def __init__(self, grid_col, grid_row, rotation):  # Col/row passed inb backwards cba to fix rn lmao
        self.x = grid_col * CONFIG.TILE_SIZE
        self.y = grid_row * CONFIG.TILE_SIZE
        self.rect = pygame.Rect((self.y + CONFIG.ITEM_COLLIDER_HITBOX, self.x + CONFIG.ITEM_COLLIDER_HITBOX), (CONFIG.TILE_SIZE - (CONFIG.ITEM_COLLIDER_HITBOX * 2), CONFIG.TILE_SIZE - (CONFIG.ITEM_COLLIDER_HITBOX * 2)))
        self.type = "belt_tile"
        self.rotation = rotation

    def draw(self, display, index1, index2):
        draw(CONFIG.IMAGES[self.type], display, index1, index2, self.rotation)
        # pygame.draw.rect(display, (105, 250, 20), self.rect, 1)


class ImportTile(object):
    def __init__(self, grid_col, grid_row, rotation):  # Col/row passed inb backwards cba to fix rn lmao
        self.x = grid_col * CONFIG.TILE_SIZE
        self.y = grid_row * CONFIG.TILE_SIZE
        self.rect = pygame.Rect((self.y + CONFIG.ITEM_COLLIDER_HITBOX, self.x + CONFIG.ITEM_COLLIDER_HITBOX), (CONFIG.TILE_SIZE - (CONFIG.ITEM_COLLIDER_HITBOX * 2), CONFIG.TILE_SIZE - (CONFIG.ITEM_COLLIDER_HITBOX * 2)))
        self.type = "import_tile"
        self.rotation = rotation
        self.alive = True
        self.last_spawn = None

    def draw(self, display, index1, index2):
        draw(CONFIG.IMAGES[self.type], display, index1, index2, self.rotation)
        # pygame.draw.rect(display, (255, 40, 20), self.rect, 1)

    def spawn(self, display, spawn_cooldown):
        time = pygame.time.get_ticks()
        if self.last_spawn:
            if time - self.last_spawn >= spawn_cooldown * 1000:
                if im.active_items:
                    legal_spawn = True
                    for item in im.active_items:
                        last_item = item.rect
                        dist = calc_dist([last_item.x, last_item.y], [self.rect.x, self.rect.y])
                        if dist < 40:
                            legal_spawn = False
                    if legal_spawn:
                        self.last_spawn = time
                        im.spawn_ore(display, self.rotation, self.x // CONFIG.TILE_SIZE, self.y // CONFIG.TILE_SIZE)
                    else:
                        self.last_spawn = time
                else:
                    self.last_spawn = time
                    im.spawn_ore(display, self.rotation, self.x // CONFIG.TILE_SIZE, self.y // CONFIG.TILE_SIZE)
        else:
            self.last_spawn = time


class ExportTile(object):
    def __init__(self, grid_col, grid_row, rotation):  # Col/row passed inb backwards cba to fix rn lmao
        self.x = grid_col * CONFIG.TILE_SIZE
        self.y = grid_row * CONFIG.TILE_SIZE
        self.rect = pygame.Rect((self.y + CONFIG.ITEM_COLLIDER_HITBOX, self.x + CONFIG.ITEM_COLLIDER_HITBOX), (CONFIG.TILE_SIZE - (CONFIG.ITEM_COLLIDER_HITBOX * 2), CONFIG.TILE_SIZE - (CONFIG.ITEM_COLLIDER_HITBOX * 2)))
        self.type = "export_tile"
        self.rotation = rotation
        self.alive = True

    def draw(self, display, index1, index2):
        draw(CONFIG.IMAGES[self.type], display, index1, index2, self.rotation)
        # pygame.draw.rect(display, (255, 40, 20), self.rect, 1)

    def func(self):
        return "export"


class SimpleUpgraderTile(object):
    def __init__(self, grid_col, grid_row, rotation):  # Col/row passed inb backwards cba to fix rn lmao
        self.x = grid_col * CONFIG.TILE_SIZE
        self.y = grid_row * CONFIG.TILE_SIZE
        self.rect = pygame.Rect((self.y + CONFIG.ITEM_COLLIDER_HITBOX, self.x + CONFIG.ITEM_COLLIDER_HITBOX), (CONFIG.TILE_SIZE - (CONFIG.ITEM_COLLIDER_HITBOX * 2), CONFIG.TILE_SIZE - (CONFIG.ITEM_COLLIDER_HITBOX * 2)))
        self.type = "simple_upgrader_tile"
        self.rotation = rotation
        self.base_add = 5
        self.upgrade_cap = 1

    def draw(self, display, index1, index2):
        draw(CONFIG.IMAGES[self.type], display, index1, index2, self.rotation)
        # pygame.draw.rect(display, (105, 250, 20), self.rect, 1)

    def func(self, start_value):
        new_value = start_value + self.base_add
        print("adding")
        return new_value


class ElectricUpgraderTile(object):
    def __init__(self, grid_col, grid_row, rotation):  # Col/row passed inb backwards cba to fix rn lmao
        self.x = grid_col * CONFIG.TILE_SIZE
        self.y = grid_row * CONFIG.TILE_SIZE
        self.rect = pygame.Rect((self.y + CONFIG.ITEM_COLLIDER_HITBOX, self.x + CONFIG.ITEM_COLLIDER_HITBOX), (CONFIG.TILE_SIZE - (CONFIG.ITEM_COLLIDER_HITBOX * 2), CONFIG.TILE_SIZE - (CONFIG.ITEM_COLLIDER_HITBOX * 2)))
        self.type = "electric_upgrader_tile"
        self.rotation = rotation

    def draw(self, display, index1, index2):
        draw(CONFIG.IMAGES[self.type], display, index1, index2, self.rotation)
        # pygame.draw.rect(display, (105, 250, 20), self.rect, 1)

