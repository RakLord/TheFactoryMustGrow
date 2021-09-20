import tiles.simple_upgrader_tile
from CONFIG import *
import grid_manager as gm
import item_manager as im
import text

import random

# Upgrades / variables


spawn_cooldown = 4
belt_speed = 3  # Lower = Faster
item_cap = 10

available_buildings = [tiles.belt_tile.BeltTile,
                       tiles.simple_upgrader_tile.SimpleUpgraderTile,
                       tiles.electric_upgrader_tile.ElectricUpgraderTile,
                       tiles.import_tile.ImportTile,
                       tiles.export_tile.ExportTile]


# Funcs

class Ui:
    def __init__(self, display, start_x, start_y):
        self.display = display
        self.start_pos = self.start_x, self.start_y = start_x, start_y
        self.buttons = []
        self.texts = []
        self.small_font = text.Font("./images/small_font.png")
        self.large_font = text.Font("./images/large_font.png")

    class Button(object):
        def __init__(self, button_image, x, y, ui_x, ui_y):
            self.image = button_image
            self.x = x + ui_x
            self.y = y + ui_y
            self.pos = (self.x, self.y)
            self.rect = pygame.Rect((self.x, self.y), (self.image.get_width(), self.image.get_height()))
            self.clicked = False

        def click(self, mouse_x, mouse_y):
            if self.rect.collidepoint((mouse_x, mouse_y)):
                self.clicked = True
            else:
                self.clicked = False

    class Text(object):
        def __init__(self, new_text, x, y, ui_x, ui_y):
            self.text = new_text
            self.x = x + ui_x
            self.y = y + ui_y
            self.pos = (self.x, self.y)

    def add_button(self, button_image, x, y):
        self.buttons.append(self.Button(button_image, x, y, self.start_x, self.start_y))

    def add_text(self, new_text, x, y):
        self.texts.append(self.Text(new_text, x, y, self.start_x, self.start_y))

    def draw(self):
        for item in self.buttons:
            self.display.blit(item.image, item.pos)
            # pygame.draw.rect(self.display, (245, 250, 200), item.rect, 1)

        for item in self.texts:
            self.large_font.render(self.display, item.text, item.pos)


def output_number(number):
    num_out = None
    if number > 1000000:
        num_out = "{:.2e}".format(number)
    else:
        num_out = number
    return num_out


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
    display_ui = Ui(display, 0, WINDOW_HEIGHT - 256 - 10)
    display_ui.add_button(IMAGES["upgrades_btn"], WINDOW_WIDTH - 68, (UI_BUTTON_HEIGHT + UI_PADDING) * 0)
    display_ui.add_button(IMAGES["inventory_btn"], WINDOW_WIDTH - 68, (UI_BUTTON_HEIGHT + UI_PADDING) * 1)
    display_ui.add_button(IMAGES["prestige_btn"], WINDOW_WIDTH - 68, (UI_BUTTON_HEIGHT + UI_PADDING) * 2)

    display_ui.add_text("Money: 0", 8, 0)

    game_loop = True
    game_grid = gm.new_game_grid()
    selected = 0
    rotation = 0

    money = 10

    while game_loop:
        display.fill(colors["gray"])
        draw_grid(game_grid, display, rotation)
        draw_items(im.active_items, display)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        for button in display_ui.buttons:
            button.click(mouse_x, mouse_y)

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

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if display_ui.buttons[0].clicked:  # Upgrades Btn
                        pass
                    if display_ui.buttons[1].clicked:  # Inventory Btn
                        pass
                    if display_ui.buttons[2].clicked:  # Prestige Btn
                        pass

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




        draw_highlight(display, pygame.mouse.get_pos(), selected_building, rotation)
        display_ui.texts[0].text = f"Money: {output_number(money)}"
        display_ui.draw()
        surf = pygame.transform.scale(display, WINDOW_SIZE)
        screen.blit(surf, (0, 0))
        pygame.display.update()
        GAME_CLOCK.tick(FPS)


game()
