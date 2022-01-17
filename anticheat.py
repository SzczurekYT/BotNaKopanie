from javascript import require, once, On, AsyncTask
from threading import Thread
import time

from minerbot import MinerBot

# Get login data
print("\033[H\033[J", end="")
username = input("Your email: ")
print("\033[H\033[J", end="")
password = input("Your password: ")
print("\033[H\033[J", end="")
# username = "WinterWolf"
# password = ""


# Import
mineflayer = require("mineflayer")
viewer = require("prismarine-viewer").mineflayer

print("Creating bot")

bot = mineflayer.createBot(
    {
        "host": "thevoid.pl",
        "port": 25565,
        "username": username,
        "password": password,
        "hideErrors": False,
        "auth": "microsoft",
    }
)

print("Waiting to log in")

# Wait to login
once(bot, "login")
print("Joined the server")

# Launch the viewer
viewer(bot, {"port": 3000, "firstPerson": True})

# Add listeners

# Handle errors
@On(bot, "error")
def error(this, err):
    print("Error")
    print(err)


# Handle kick
@On(bot, "kicked")
def kick(this, reason, loggedIn):
    print("Kick with reason: ")
    print(reason)


# Accept the resourcepack
@On(bot, "resourcePack")
def acceptResourcepack(this, url, hash):
    print("Accepting resourcepack!")
    bot.acceptResourcePack()


# Wait to make sure everything is loaded.
time.sleep(2)

# Let's trigger an antycheat ; )

# Get bot yaw
yaw = bot.entity.yaw

for _ in range(3):
    # Look down
    bot.look(yaw, -90, True)
    print("Look down")
    time.sleep(1)

    # Look up (forward)
    bot.look(yaw, 0, True)
    print("Look up")
    time.sleep(1)


# Prevent script from finishing
while True:
    input = input("Wpisz stop aby zakończyć kopanie!: \n")
    if input == "stop":
        bot.quit()
        exit(0)

