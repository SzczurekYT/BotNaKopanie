from javascript import require, On
import time

mineflayer = require("mineflayer")


class MinerBot:
    def __init__(self, username, password) -> None:
        try:
            self.bot = mineflayer.createBot(
                {
                    "host": "localhost",
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
            print("Bot: Wziąłem kolejny kilof.")
            self.bot.equip(tool, "hand")

    def makeCobblex(self):
        self.bot.chat("/cx")

    def emptyInventory(self, cobblex: bool):

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
            self.bot.look(yaw, -1.57, True)
            # time.sleep(1)

            # Drop items
            for item in toDrop:
                if item["type"] == 686:
                    self.bot.toss(item["type"], None, item["count"] - 5)
                else:
                    self.bot.tossStack(item)
                # time.sleep(0.1)

            # Look up (forward)
            self.bot.look(yaw, 0, True)
            # time.sleep(1)

    def repairPick(self):
        diamonds = self.bot.inventory.findInventoryItem(686)
        if not diamonds:
            return
        block = self.bot.findBlock({"matching": [341, 340, 339], "maxDistance": 4})
        if block:
            anvil = self.bot.openAnvil(block)
            anvil.combine(self.bot.heldItem, diamonds)

