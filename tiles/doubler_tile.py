from CONFIG import *
from utils import *


class DoublerTile(object):
    def __init__(self, grid_col, grid_row, rotation):  # Col/row passed inb backwards cba to fix rn lmao
        self.x = grid_col * CONFIG.TILE_SIZE
        self.y = grid_row * CONFIG.TILE_SIZE
        self.rect = pygame.Rect((self.y + CONFIG.ITEM_COLLIDER_HITBOX, self.x + CONFIG.ITEM_COLLIDER_HITBOX), (CONFIG.TILE_SIZE - (CONFIG.ITEM_COLLIDER_HITBOX * 2), CONFIG.TILE_SIZE - (CONFIG.ITEM_COLLIDER_HITBOX * 2)))
        self.type = "doubler_tile"
        self.rotation = rotation
        self.upgrade_cap = 1

    def draw(self, display, index1, index2):
        draw(CONFIG.IMAGES[self.type], display, index1, index2, self.rotation)
        if CONFIG.DRAW_COLLIDERS:
            pygame.draw.rect(display, (105, 250, 20), self.rect, 1)

    def func(self, display):
        possible_rotations = [-1, 1]
        rotation = possible_rotations[random.randint(0, 1)]
        return rotation
