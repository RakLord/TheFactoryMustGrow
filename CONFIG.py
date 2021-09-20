import pygame
from pygame.locals import *
import sys
import random
import math
import inventory_manager as inv
import item_manager as im
import grid_manager as gm
import ui_manager as ui
import prestige_manager as pm
from utils import *
import tiles
from tiles import belt_tile
from tiles import electric_upgrader_tile
from tiles import empty_tile
from tiles import export_tile
from tiles import import_tile
from tiles import simple_upgrader_tile
from tiles import locked_tile
from tiles import enhancer_tile
from tiles import doubler_tile
from tiles import tripler_tile


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
          "orange": (255, 203, 154),
          "metal": (209, 232, 226)}

# Images
IMAGES = {"empty_tile": pygame.image.load("images/empty_tile.png"),
          "belt_tile": pygame.image.load("images/belt_tile.png"),
          "import_tile": pygame.image.load("images/import_tile.png"),
          "iron_ore": pygame.image.load("images/iron_clump.png"),
          "simple_upgrader_tile": pygame.image.load("images/simple_upgrader_tile.png"),
          "electric_upgrader_tile": pygame.image.load("images/electric_upgrader_tile.png"),
          "export_tile": pygame.image.load("images/export_tile.png"),
          "upgrades_btn": pygame.image.load("images/btn_upgrades.png"),
          "prestige_btn": pygame.image.load("images/btn_prestige.png"),
          "inventory_btn": pygame.image.load("images/btn_inventory.png"),
          "locked_tile": pygame.image.load("images/locked_tile.png"),
          "expand_btn": pygame.image.load("images/btn_expand.png"),
          "buy_btn": pygame.image.load("images/btn_buy.png"),
          "enhancer_tile": pygame.image.load("images/enhancer_tile.png"),
          "doubler_tile": pygame.image.load("images/doubler_tile.png"),
          "trippler_tile": pygame.image.load("images/trippler_tile.png")}

