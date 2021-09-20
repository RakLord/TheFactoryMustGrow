from CONFIG import *
from utils import *



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
