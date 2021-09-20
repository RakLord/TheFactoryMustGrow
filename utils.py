import CONFIG
from CONFIG import *
import math


def draw(building_type, display, index1, index2, rotation):
    if rotation == 0:
        display.blit(building_type, (index2 * CONFIG.TILE_SIZE, index1 * CONFIG.TILE_SIZE))
    if rotation == 1:
        display.blit(pygame.transform.rotate(building_type, 90), (index2 * CONFIG.TILE_SIZE, index1 * CONFIG.TILE_SIZE))
    if rotation == 2:
        display.blit(pygame.transform.rotate(building_type, 180), (index2 * CONFIG.TILE_SIZE, index1 * CONFIG.TILE_SIZE))
    if rotation == 3:
        display.blit(pygame.transform.rotate(building_type, 270), (index2 * CONFIG.TILE_SIZE, index1 * CONFIG.TILE_SIZE))


def calc_dist(obj_1, obj_2):  # Calculates the vector between 2 objects
    dist = math.hypot(obj_1[0] - obj_2[0], obj_1[1] - obj_2[1])
    return dist


def output_number(number):
    num_out = None
    if number > 1000000:
        num_out = "{:.2e}".format(number)
    else:
        num_out = number
    return num_out