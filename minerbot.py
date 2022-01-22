import math
from javascript import require, On
import time

mineflayer = require("mineflayer")


class MinerBot:
    def __init__(self, username, password) -> None:
        try:
            self.bot = mineflayer.createBot(
                {
                    "host": "thevoid.pl",
                    "port": 25565,
                    "username": username,
                    "password": password,
                    "hideErrors": False,
                    "auth": "microsoft",
                }
            )
        except Exception as e:
            print("Z jakiegoś powodu nie udało się połączyć!")

    def launchViewer(self):
        viewer = require("prismarine-viewer").mineflayer
        viewer(self.bot, {"port": 3000, "firstPerson": True})
        print("Podgląd włączony.")

    def equipPick(self):
        tool = self.bot.inventory.findInventoryItem(721)
        if tool:
            self.bot.equip(tool, "hand")

    def makeCobblex(self):
        # Send /cx command that creates cobbleX
        self.bot.chat("/cx")

    def emptyInventory(self, cobblex: bool):

        print("Dropping inventory!")

        # Ids of items to drop
        ids = [684, 585, 692, 696, 687, 686, 792, 235, 734, 234]

        # If bot doesn't make cobblex then it should also drop cobblestone
        if not cobblex:
            ids.append(21)

        # Get all items to drop
        toDrop = self.bot.inventory.items()
        toDrop = list(filter(lambda item: item["type"] in ids, toDrop))

        # If there is anython to drop than drop it
        if toDrop:
            # Get bot yaw
            yaw = self.bot.entity.yaw

            # Look down
            self.bot.look(yaw, -math.pi / 2, True)
            time.sleep(1)

            # Drop items
            for item in toDrop:
                if item["type"] == 686:
                    if item.count >= 5:
                        self.bot.toss(686, None, item.count - 4)
                else:
                    self.bot.tossStack(item)
                time.sleep(0.3)
            # Look up (forward)
            self.bot.look(yaw, 0, True)
            time.sleep(1)
            print("Dropped all items!")

    def repairPick(self) -> bool:
        print("Próbuję naprawić kilof.")
        yaw = self.bot.entity.yaw
        pitch = self.bot.entity.pitch
        diamonds = self.bot.inventory.findInventoryItem(686)
        if not diamonds:
            return
        block = self.bot.findBlock({"matching": [341, 340, 339], "maxDistance": 5})
        if block:
            anvil = self.bot.openAnvil(block)
            try:
                anvil.combine(self.bot.heldItem, diamonds)
            except Exception as e:
                print("Nie udało się naprawić kilofa.")
                self.bot.look(yaw, pitch, True)
                return False
                
            print("Naprawiono kilof.")
            anvil.close()
            self.equipPick()
            self.bot.look(yaw, pitch, True)
            time.sleep(1)
            return True
        else:
            print("Brak kowadła, nie naprawiono kilofa.")
            return False

