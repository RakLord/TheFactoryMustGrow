import CONFIG
from CONFIG import *
import tiles


class Inventory:
    def __init__(self):
        self.selected_item_index = 0
        self.inventory = [{"item": tiles.belt_tile.BeltTile, "quantity": 4},
                          {"item": tiles.export_tile.ExportTile, "quantity": 1}]
        self.selected_item = None
        self.selected_item_quantity = 4

    def next_item(self):
        if self.selected_item_index < len(self.inventory) - 1:
            self.selected_item_index += 1
        else:
            self.selected_item_index = 0

        self.selected_item = self.inventory[self.selected_item_index]["item"]
        self.selected_item_quantity = self.inventory[self.selected_item_index]["quantity"]

    def place_item(self):
        self.inventory[self.selected_item_index]["quantity"] -= 1
        self.selected_item_quantity = self.inventory[self.selected_item_index]["quantity"]
