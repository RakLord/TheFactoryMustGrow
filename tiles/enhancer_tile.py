from CONFIG import *
from utils import *


class EnhancerTile(object):
    def __init__(self, grid_col, grid_row, rotation):  # Col/row passed inb backwards cba to fix rn lmao
        self.x = grid_col * CONFIG.TILE_SIZE
        self.y = grid_row * CONFIG.TILE_SIZE
        self.rect = pygame.Rect((self.y + CONFIG.ITEM_COLLIDER_HITBOX, self.x + CONFIG.ITEM_COLLIDER_HITBOX), (CONFIG.TILE_SIZE - (CONFIG.ITEM_COLLIDER_HITBOX * 2), CONFIG.TILE_SIZE - (CONFIG.ITEM_COLLIDER_HITBOX * 2)))
        self.type = "enhancer_tile"
        self.rotation = rotation
        self.item_multiplier = 1.25
        self.upgrade_cap = 3

    def draw(self, display, index1, index2):
        draw(CONFIG.IMAGES[self.type], display, index1, index2, self.rotation)
        if CONFIG.DRAW_COLLIDERS:
            pygame.draw.rect(display, (105, 250, 40), self.rect, 1)

    def func(self, start_value):
        new_value = start_value * self.item_multiplier
        return new_value
