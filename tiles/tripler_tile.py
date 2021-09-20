from CONFIG import *
from utils import *


class TriplerTile(object):
    def __init__(self, grid_col, grid_row, rotation):  # Col/row passed inb backwards cba to fix rn lmao
        self.x = grid_col * CONFIG.TILE_SIZE
        self.y = grid_row * CONFIG.TILE_SIZE
        self.rect = pygame.Rect((self.y + CONFIG.ITEM_COLLIDER_HITBOX, self.x + CONFIG.ITEM_COLLIDER_HITBOX), (CONFIG.TILE_SIZE - (CONFIG.ITEM_COLLIDER_HITBOX * 2), CONFIG.TILE_SIZE - (CONFIG.ITEM_COLLIDER_HITBOX * 2)))
        self.type = "tripler_tile"
        self.rotation = rotation
        self.base_add = 5
        self.upgrade_cap = 5

    def draw(self, display, index1, index2):
        draw(CONFIG.IMAGES[self.type], display, index1, index2, self.rotation)
        if CONFIG.DRAW_COLLIDERS:
            pygame.draw.rect(display, (105, 250, 20), self.rect, 1)

    def func(self, start_value):
        new_value = start_value + self.base_add
        return new_value
