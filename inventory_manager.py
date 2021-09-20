import CONFIG
from CONFIG import *
import tiles


class Inventory:
    def __init__(self):
        self.selected_item_index = 0
        self.inventory = [{"item": tiles.belt_tile.BeltTile, "quantity": 4, "max_quantity": 4, "name": "BeltTile", "base_price": 5, "description": "Moves items around the factory"},
                          {"item": tiles.export_tile.ExportTile, "quantity": 1, "max_quantity": 1, "name": "ExportTile", "base_price": 50, "description": "Exports items for money"},
                          {"item": tiles.simple_upgrader_tile.SimpleUpgraderTile, "quantity": 1, "max_quantity": 1, "name": "SimpleUpgraderTile", "base_price": 100, "description": "Upgrades ores. Max 1"}]

        self.available_items = [{"item": tiles.belt_tile.BeltTile, "quantity": 1, "max_quantity": 1, "name": "BeltTile", "base_price": 5, "description": "Moves items around the factory"},
                                {"item": tiles.export_tile.ExportTile, "quantity": 1,  "max_quantity": 1, "name": "ExportTile", "base_price": 100, "description": "Exports items for money!"},
                                {"item": tiles.simple_upgrader_tile.SimpleUpgraderTile, "quantity": 1, "max_quantity": 1, "name": "SimpleUpgraderTile", "base_price": 100, "description": "Upgrades ores.Max 1"}]

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

    def add_item(self, item, to_max=False):
        for index, items in enumerate(self.inventory):
            print(items, index)
            if items["name"] == item:
                items["quantity"] += 1
                if to_max:
                    items["quantity"] += 1
                    items["max_quantity"] += 1
        else:
            for index, items in enumerate(self.available_items):
                if items["name"]:
                    self.inventory.append(self.available_items[index])

        self.selected_item_quantity = self.inventory[self.selected_item_index]["quantity"]



