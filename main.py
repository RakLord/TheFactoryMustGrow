from CONFIG import *
import grid_manager as gm
import item_manager as im
import text

import random

# Upgrades / variables


spawn_cooldown = 4
belt_speed = 3  # Lower = Faster
item_cap = 10

available_buildings = [BeltTile, SimpleUpgraderTile, ElectricUpgraderTile, ImportTile, ExportTile]


# Funcs

def cycle_selected(selected):
    if selected < len(available_buildings) - 1:
        selected += 1
    else:
        selected = 0
    return selected


def draw_grid(game_grid, display, rotation):
    for index1, row in enumerate(game_grid):
        for index2, tile in enumerate(row):
            tile.draw(display, index1, index2)


def draw_items(active_items, display):
    for item in active_items:
        item.draw(display)


def get_mouse_grid_pos(mouse_pos):
    mouse_x, mouse_y = mouse_pos
    mouse_grid_x = mouse_x // TILE_SIZE
    mouse_grid_y = mouse_y // TILE_SIZE
    # print(f"MGX: {mouse_grid_x} / {GRID_WIDTH}\nMGY: {mouse_grid_y} / {GRID_HEIGHT}\n======")
    if mouse_grid_x < GRID_WIDTH and mouse_grid_y < GRID_HEIGHT:
        return mouse_grid_y, mouse_grid_x


def draw_highlight(display, mouse_pos, selected_building, rotation):
    grid_mouse_pos = get_mouse_grid_pos(mouse_pos)
    if grid_mouse_pos:
        row, col = grid_mouse_pos
        # print(row, col)

        hover_building = selected_building(1, 1, rotation)  # First 2 params dont matter as we only need object.type
        if rotation == 0:
            display.blit(IMAGES[hover_building.type], (col * TILE_SIZE, row * TILE_SIZE), special_flags=BLEND_RGB_ADD)
        if rotation == 1:
            display.blit(pygame.transform.rotate(IMAGES[hover_building.type], 90), (col * TILE_SIZE, row * TILE_SIZE),
                         special_flags=BLEND_RGB_ADD)
        if rotation == 2:
            display.blit(pygame.transform.rotate(IMAGES[hover_building.type], 180), (col * TILE_SIZE, row * TILE_SIZE),
                         special_flags=BLEND_RGB_ADD)
        if rotation == 3:
            display.blit(pygame.transform.rotate(IMAGES[hover_building.type], 270), (col * TILE_SIZE, row * TILE_SIZE),
                         special_flags=BLEND_RGB_ADD)


def game():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
    display = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

    game_loop = True
    game_grid = gm.new_game_grid()
    selected = 0

    rotation = 0

    money = 10

    small_font = text.Font("./images/small_font.png")
    large_font = text.Font("./images/large_font.png")

    while game_loop:
        display.fill(colors["gray"])
        draw_grid(game_grid, display, rotation)
        draw_items(im.active_items, display)
        
        large_font.render(display, f"Money: {money}", (20, GRID_HEIGHT * TILE_SIZE + TILE_SIZE))

        selected_building = available_buildings[selected]
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    if rotation > 0:
                        rotation -= 1
                    else:
                        rotation = 3
                if event.key == K_SPACE:
                    selected = cycle_selected(selected)

        if pygame.mouse.get_pressed()[0]:
            tile_clicked = get_mouse_grid_pos(pygame.mouse.get_pos())
            if tile_clicked:
                gm.place_object(game_grid, tile_clicked, selected_building, rotation)

        if pygame.mouse.get_pressed()[2]:
            tile_clicked = get_mouse_grid_pos(pygame.mouse.get_pos())
            if tile_clicked:
                gm.place_object(game_grid, tile_clicked, EmptyTile, rotation)

        for row in range(0, GRID_HEIGHT):
            for col in range(0, GRID_WIDTH):
                tile = game_grid[row][col]
                if tile.type == "import_tile" and len(im.active_items) < item_cap:
                    tile.spawn(display, spawn_cooldown)

        for item in im.active_items:
            state = item.tick(belt_speed_value=belt_speed, building_grid=game_grid)
            if state:
                if state[0] == "dead":
                    im.active_items.remove(item)
                elif state[0] == "export":
                    money += item.value
                    im.active_items.remove(item)

        # print(money)

        draw_highlight(display, pygame.mouse.get_pos(), selected_building, rotation)
        surf = pygame.transform.scale(display, WINDOW_SIZE)
        screen.blit(surf, (0, 0))
        pygame.display.update()
        GAME_CLOCK.tick(FPS)


game()
