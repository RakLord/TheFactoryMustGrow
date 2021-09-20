import CONFIG
from CONFIG import *
import tiles
import math


class Prestige:
    def __init__(self):
        self.prestige_item_pool = [{"item": tiles.belt_tile.BeltTile, "quantity": 1, "max_quantity": 1, "name": "BeltTile", "base_price": 5, "description": "Moves items around the factory", "rarity": 10},
                                   {"item": tiles.export_tile.ExportTile, "quantity": 1,  "max_quantity": 1, "name": "ExportTile", "base_price": 100, "description": "Exports items for money!", "rarity": 10},
                                   {"item": tiles.simple_upgrader_tile.SimpleUpgraderTile, "quantity": 1, "max_quantity": 1, "name": "SimpleUpgraderTile", "base_price": 100, "description": "Upgrades ores.Max 1", "rarity": 10},
                                   {"item": tiles.electric_upgrader_tile.ElectricUpgraderTile, "quantity": 1, "max_quantity": 1, "name": "ElectricUpgraderTile", "base_price": 600, "description": "Activates ores with electricity", "rarity": 10},
                                   {"item": tiles.enhancer_tile.EnhancerTile, "quantity": 1, "max_quantity": 1, "name": "EnhancerTile", "base_price": 1000, "description": "Enhances ores by a percent of their value", "rarity": 10}]

        self.full_item_pool = []  # Contains ultra high quality items (from later prestige when added)
        self.prestige_value = 1

    def calc_prestige_value(self, money):
        self.prestige_value = (money / 100000) ** 0.5
        return self.prestige_value

    def pick_new_item(self):
        random_value = random.randint(1, 50)
        random_value = random_value + math.log10(self.prestige_value)

        for attempts in range(0, 20):
            item_try = random.randint(0, len(self.prestige_item_pool) - 1)
            item_rarity = self.prestige_item_pool[item_try]["rarity"]
            if random_value >= item_rarity:
                return self.prestige_item_pool[item_try]

        else:
            return self.prestige_item_pool[0]


