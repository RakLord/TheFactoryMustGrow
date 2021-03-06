import tiles.electric_upgrader_tile
from CONFIG import *

import text_manager

import random

# Upgrades / variables


spawn_cooldown = 4
belt_speed = 3  # Lower = Faster
item_cap = 10


tile_images = {tiles.belt_tile.BeltTile: IMAGES["belt_tile"],
               tiles.electric_upgrader_tile.ElectricUpgraderTile: IMAGES["electric_upgrader_tile"],
               tiles.empty_tile.EmptyTile: IMAGES["empty_tile"],
               tiles.export_tile.ExportTile: IMAGES["export_tile"],
               tiles.import_tile.ImportTile: IMAGES["import_tile"],
               tiles.simple_upgrader_tile.SimpleUpgraderTile: IMAGES["simple_upgrader_tile"],
               tiles.enhancer_tile.EnhancerTile: IMAGES["enhancer_tile"],
               tiles.doubler_tile.DoublerTile: IMAGES["doubler_tile"],
               tiles.tripler_tile.TriplerTile: IMAGES["trippler_tile"]}

# Funcs


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

        hover_building = selected_building(1, 1, rotation)  # First 2 params don't matter as we only need object.type
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


def get_item_price(item):
    return round(item["base_price"] * item["max_quantity"] ** 3)


def game():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
    display = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    display_ui = ui.Ui(display, 0, WINDOW_HEIGHT - 256 - 10)
    display_ui.add_button(IMAGES["expand_btn"], WINDOW_WIDTH - 68, (UI_BUTTON_HEIGHT + UI_PADDING) * 0)
    display_ui.add_button(IMAGES["inventory_btn"], WINDOW_WIDTH - 68, (UI_BUTTON_HEIGHT + UI_PADDING) * 1)
    display_ui.add_button(IMAGES["prestige_btn"], WINDOW_WIDTH - 68, (UI_BUTTON_HEIGHT + UI_PADDING) * 2)
    display_ui.add_button(IMAGES["buy_btn"], 8, 180)

    display_ui.add_image(IMAGES["empty_tile"], 8, 220)

    display_ui.add_text("Money: 0", 8, 0)
    display_ui.add_text("Expand Cost: 0", 8, 18)
    display_ui.add_text("x1", 44, 228)
    display_ui.add_text("Cost: 10", 8, 160)
    display_ui.add_text("", 100, 228)
    display_ui.add_text("Prestige Value: 0", 8, 36)

    game_loop = True
    game_grid = gm.new_game_grid()
    rotation = 0

    prestige = pm.Prestige()
    grid_expand_base_price = 100
    grid_expand_level = 0  # Button level
    grid_unlocked_level = 4  # Actual unlocked space (not button level)
    gm.locked_tiles(game_grid, grid_unlocked_level)

    prestige_level = 0
    prestige_base_cost = 100000

    inventory = inv.Inventory()
    inventory.selected_item = inventory.inventory[0]["item"]
    money = 10

    while game_loop:
        display.fill(colors["gray"])
        draw_grid(game_grid, display, rotation)
        draw_items(im.active_items, display)

        expand_price = round(grid_expand_base_price * grid_expand_level ** 3)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        for button in display_ui.buttons:
            button.click(mouse_x, mouse_y)

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
                    inventory.next_item()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if display_ui.buttons[0].clicked:  # Expand Btn
                        if money > expand_price:
                            gm.locked_tiles(game_grid, grid_unlocked_level + 1)
                            money -= expand_price
                            grid_expand_level += 1
                            grid_unlocked_level += 1
                    elif display_ui.buttons[1].clicked:  # Inventory Btn
                        pass
                    elif display_ui.buttons[2].clicked:  # Prestige Btn
                        if prestige.prestige_value >= 1:
                            prestige.prestige_value += (money / prestige_base_cost) ** 0.5
                            money = 0
                            inventory.add_item(prestige.pick_new_item())
                    elif display_ui.buttons[3].clicked:
                        if money > get_item_price(inventory.inventory[inventory.selected_item_index]):
                            money -= get_item_price(inventory.inventory[inventory.selected_item_index])
                            inventory.add_item(inventory.inventory[inventory.selected_item_index]["name"], True)

        if pygame.mouse.get_pressed()[0]:
            tile_clicked = get_mouse_grid_pos(pygame.mouse.get_pos())
            if tile_clicked:
                if type(game_grid[tile_clicked[0]][tile_clicked[1]]).__name__ not in ["LockedTile", "ImportTile"]:
                    if inventory.selected_item_quantity > 0:
                        if inventory.inventory[inventory.selected_item_index]["name"] != type(game_grid[tile_clicked[0]][tile_clicked[1]]).__name__:
                            inventory.place_item()
                            gm.place_object(game_grid, tile_clicked, inventory.selected_item, rotation)

        if pygame.mouse.get_pressed()[2]:
            tile_clicked = get_mouse_grid_pos(pygame.mouse.get_pos())
            if tile_clicked:
                if type(game_grid[tile_clicked[0]][tile_clicked[1]]).__name__ not in ["EmptyTile", "LockedTile", "ImportTile"]:
                    if type(game_grid[tile_clicked[0]][tile_clicked[1]]).__name__ != "EmptyTile":
                        inventory.add_item(type(game_grid[tile_clicked[0]][tile_clicked[1]]).__name__)
                        gm.place_object(game_grid, tile_clicked, tiles.empty_tile.EmptyTile, rotation)

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

        draw_highlight(display, pygame.mouse.get_pos(), inventory.selected_item, rotation)
        display_ui.texts[0].text = f"Money: {output_number(money)}"
        display_ui.texts[1].text = f"Expand price: {output_number(expand_price)}"
        display_ui.texts[2].text = f'x{inventory.selected_item_quantity}'
        display_ui.texts[3].text = f"Cost: {get_item_price(inventory.inventory[inventory.selected_item_index])}"
        display_ui.texts[4].text = f"{inventory.inventory[inventory.selected_item_index]['description']}"
        display_ui.texts[5].text = f"Prestige Value: {output_number(prestige.calc_prestige_value(money))}"
        display_ui.images[0].image = tile_images[inventory.selected_item]
        display_ui.draw()
        surf = pygame.transform.scale(display, WINDOW_SIZE)
        screen.blit(surf, (0, 0))
        pygame.display.update()
        GAME_CLOCK.tick(FPS)


game()
