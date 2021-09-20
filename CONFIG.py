import pygame
from pygame.locals import *
import sys
import random
import math
import item_manager as im
import grid_manager as gm
import ui_manager as ui
import tiles
from tiles import belt_tile
from tiles import electric_upgrader_tile
from tiles import empty_tile
from tiles import export_tile
from tiles import import_tile
from tiles import simple_upgrader_tile


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080
FPS = 60
TILE_SIZE = 32

GRID_WIDTH = WINDOW_WIDTH // TILE_SIZE
GRID_HEIGHT = (WINDOW_HEIGHT - 256) // TILE_SIZE

UI_START = WINDOW_HEIGHT - (WINDOW_HEIGHT - WINDOW_WIDTH)
UI_BUTTON_SIZE = UI_BUTTON_WIDTH, UI_BUTTON_HEIGHT = 64, 32
UI_PADDING = 4
GAME_CLOCK = pygame.time.Clock()


ITEM_COLLIDER_HITBOX = 12  # higher = smaller

DRAW_COLLIDERS = False

colors = {"gray": (44, 53, 49),
          "blue": (17, 100, 102),
          "peach": (217, 176, 140),
          "orrange": (255, 203, 154),
          "metal": (209, 232, 226)}

#### Images ####
IMAGES = {"empty_tile": pygame.image.load("images/empty_tile.png"),
          "belt_tile": pygame.image.load("images/belt_tile.png"),
          "import_tile": pygame.image.load("images/import_tile.png"),
          "iron_ore": pygame.image.load("images/iron_clump.png"),
          "simple_upgrader_tile": pygame.image.load("images/simple_upgrader_tile.png"),
          "electric_upgrader_tile": pygame.image.load("images/electric_upgrader_tile.png"),
          "export_tile": pygame.image.load("images/export_tile.png"),
          "upgrades_btn": pygame.image.load("images/btn_upgrades.png"),
          "prestige_btn": pygame.image.load("images/btn_prestige.png"),
          "inventory_btn": pygame.image.load("images/btn_inventory.png")}

