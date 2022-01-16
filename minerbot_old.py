from javascript import require, once, On
import time
import sys


username = input("Podaj email: ")
password = input("Podaj hasło: ")
print("\033[H\033[J", end="")
# username = "WinterWolf"
# password = ""

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


mineflayer = require("mineflayer")
viewer = require('prismarine-viewer').mineflayer

print("Tworzę bota")

try:
    bot = mineflayer.createBot(
        {
            "host": "thevoid.pl",
            "port": 25565,
            "username": username,
            "password": password,
            "hideErrors": False,
            "auth": "microsoft",
            # "checkTimeoutInterval": 60*1000
        }
)
except Exception as e:
    print("Z jakiegoś powodu nie udało się połączyć!")

print("Bot utworzony")

@On(bot, "error")
def error(this, err):
    print("Error")
    print(err)

@On(bot, "kicked")
def kick(this, reason, loggedIn):
    print("Kick")
    print(reason)
    print(loggedIn)
    sys.exit()

once(bot, "login") #Bot is stuck here
print("Wszedłem!")

viewer(bot, { "port": 3000, "firstPerson": True }) # port is the minecraft server port, if first person is false, you get a bird's-eye view
print("Widok włączony!")




@On(bot, "resourcePack")
def acceptResourcepack(this, url, hash):
    print("Akceptowanie resourcepacka!")
    bot.acceptResourcePack()

@On(bot, "death")
def die(this):
    bot.quit()
    print("Zginąłem!")
    # sys.exit()

time.sleep(2)


@On(bot, "physicsTick")
def tick(this):
    block = bot.blockAtCursor(5)
    if block == None:
        return
    if block.stateId == None:
        return
    miningBlock = bot.targetDigBlock
    if miningBlock == None:
        return

    if block.position.toString() != miningBlock.position.toString():
        bot.stopDigging()
        
        
        
def makeCobblex():

    if bot.inventory.count(21) >= 640:
        bot.chat("/cx")

def equipPick():

    held = bot.heldItem
    if held == None:
        tool = bot.inventory.findInventoryItem(721)
        if tool:
            print("Wziąłem kolejny kilof.")
            bot.equip(tool, "hand")
            
    else:
        if held["type"] != 721:
            bot.tossStack(held)
            tool = bot.inventory.findInventoryItem(721)
            if tool:
                print("Wziąłem kolejny kilof.")
                bot.equip(tool, "hand")

def emptyInventory():
    ids = [ 684, 585, 692, 696, 687, 686, 792, 235, 734, 234 ]
    dropCount = {
        "684": 64, # Coal
        "585": 64, # Redstone
        "692": 64, # Iron
        "696": 64, # Gold
        "687": 64, # Emerald
        "686": 32, # Diamond
        "792": 32, # Book
        "235": 16, # Obsidian
        "734": 15,  # Gunpowder 
        "21": 64,   # Cobblestone
        "234": 1 # Mossy cobblestone a.k.a. CobbleX
        }
    if not cobblex:
        ids.append(21)
    toDrop = list(bot.inventory.items())
    toDrop = filter(lambda item: item["type"] in ids, toDrop)
    if not toDrop: return
    toDrop = list(filter(lambda item: item["count"] >= dropCount[str(item["type"])], toDrop))
    if toDrop:
        yaw = bot.entity.yaw
        bot.look(yaw, -90, True)
        time.sleep(1)
        for item in toDrop:
            # if item["type"] == 686:
            #     bot.toss(item["type"], None, item["count"] - 5)
            # else:
            #     bot.tossStack(item)
            bot.tossStack(item)
            time.sleep(0.1)
        bot.look(yaw, 0, True)
        time.sleep(1)

      
print("Zaczynam kopać!")

bot.setControlState("sneak", True)

while True:

    if cobblex:
        makeCobblex()

    equipPick()
    emptyInventory()

    block = bot.blockAtCursor(5)
    if block == None:
        time.sleep(1)
        continue
    if block.stateId == None:
        time.sleep(1)
        continue

    try:
        bot.dig(block, "ignore")
    except Exception as e:
        pass

    time.sleep(0.05)

