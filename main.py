from javascript import require, once, On, AsyncTask
import time
import sys

from minerbot import MinerBot

# Get login data
print("\033[H\033[J", end="")
username = input("Podaj email: ")
print("\033[H\033[J", end="")
password = input("Podaj hasło: ")
print("\033[H\033[J", end="")
# username = "WinterWolf"
# password = ""

# Cobblex
while True:
    text = input("Czy mam automatycznie tworzyć CobbleX: (tak/nie): ")
    match text:
        case "tak":
            cobblex = True
        case "nie":
            cobblex = False
        case _:
            print("Wpisz 'tak' lub 'nie' ")
            continue
    break

# Import
mineflayer = require("mineflayer")
viewer = require('prismarine-viewer').mineflayer

# Bot creation
print("Tworzenie bota.")
minerBot = MinerBot(username, password)
print("Bot utworzony")

# Wait to login
once(minerBot.bot, "login")
print("Bot wszedłe na serwer.")

# Launch the viewer
minerBot.launchViewer()

# Add listeners

# Handle errors
@On(minerBot.bot, "error")
def error(this, err):
    print("Error")
    print(err)

# Handle kick
@On(minerBot.bot, "kicked")
def kick(this, reason, loggedIn):
    print("Kick with reason: ")
    print(reason)
    for text in reason:
        print(text)

# Accept the resourcepack
@On(minerBot.bot, "resourcePack")
def acceptResourcepack(this, url, hash):
    print("Akceptowanie resourcepacka!")
    minerBot.bot.acceptResourcePack()

# Handle death
@On(minerBot.bot, "death")
def die(this):
    minerBot.bot.quit()
    print("Bot: Zginąłem!")
    # sys.exit()

# Sneak
minerBot.bot.setControlState("sneak", True)

# Wait to make sure everything is loaded.
time.sleep(2)

# Define is mining
isMining = False

minPassed: bool = False

@AsyncTask(start=True)
def minLoop(task):
    global minPassed
    while True:
        time.sleep(15)
        minPassed = True

def miningCallback(x, y):
    global isMining
    isMining = False

# The tick
@On(minerBot.bot, "physicsTick")
def tick(this):

    global isMining
    if isMining:

        # Prevent mining throught walls
        block = minerBot.bot.blockAtCursor(5)
        if block == None:
            return
        if block.stateId == None:
            return
        miningBlock = minerBot.bot.targetDigBlock
        if not miningBlock: return

        if block.position.toString() != miningBlock.position.toString():
            minerBot.bot.stopDigging()
        
    else:
        # Equip new pick if needed
        held = minerBot.bot.heldItem
        if held == None:
            minerBot.equipPick()
        elif held["type"] != 721:
            minerBot.bot.tossStack(held)
            minerBot.equipPick()

        if minerBot.bot.inventory.count(21) >= 640:
            minerBot.makeCobblex()

        global minPassed
        if minPassed:
            minerBot.emptyInventory(cobblex)

        block = minerBot.bot.blockAtCursor(5)
        if block == None:
            return
        if block.stateId == None:
            return

        isMining = True
        try:
            minerBot.bot.dig(block, "ignore", "raycast", miningCallback)
        except Exception as e:
            pass


# print("Zaczynam kopać!")

# Prevent script from finishing
while True:
    input = input("Wpisz stop aby zakończyć kopanie!: ")
    if input == "stop":
        break

