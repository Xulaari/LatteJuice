import requests, subprocess, sys, time, psutil, os, json
from pypresence import Presence

RobloxProcName = "RobloxPlayerBet"

username = os.getenv("USER")

if not os.path.exists(f"/home/{username}/.lattejuice"):
    print(".lattejuice not found, creating dependencies.")

    os.mkdir(f"/home/{username}/.lattejuice")

    json_data = requests.get("https://raw.githubusercontent.com/Xulaari/LatteJuice/main/settings.json").text

    with open(f"/home/{username}/.lattejuice/settings.json", "w") as file:
        file.write(json_data)

file = open(f"/home/{username}/.lattejuice/settings.json", "r")

data = json.load(file)

def IsProgramOpen(program):
    if program in (i.name() for i in psutil.process_iter()):
        return True
    else:
        return False

client_id = "1137072340375707758"
RPC = Presence(client_id)

if len(sys.argv) > 1:
    keystroke = sys.argv[1].lower()
else:
    print("No argument for the game name/gameid. Usage: lattejuice <game name/placeid|edit>")
    sys.exit(0)

if keystroke in data["games"]:
    gameid = data['games'][keystroke]
    process = subprocess.Popen(
        [f"open roblox://experiences/start?placeId={gameid}"],
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setpgrp
    )
    UID = requests.get(f"https://apis.roblox.com/universes/v1/places/{data['games'][keystroke]}/universe").json()["universeId"]
elif keystroke.isdigit():
    gameid = keystroke
    process = subprocess.Popen(
        [f"open roblox://experiences/start?placeId={keystroke}"],
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setpgrp
    )
    UID = requests.get(f"https://apis.roblox.com/universes/v1/places/{keystroke}/universe").json()["universeId"]
elif keystroke == "edit":
    os.system(f"nano /home/{username}/.lattejuice/settings.json")
    sys.exit(0)
else:
    print("Invalid argument. Exiting in 3 seconds.")
    time.sleep(3)
    sys.exit(0)

GAMENAME = requests.get(f"https://games.roblox.com/v1/games?universeIds={UID}").json()["data"][0]["name"]

GAMETHUMBNAIL = requests.get(f"https://thumbnails.roblox.com/v1/games/icons?universeIds={UID}&returnPolicy=PlaceHolder&size=512x512&format=Png&isCircular=false").json()["data"][0]["imageUrl"]

GAMECREATOR = requests.get(f"https://games.roblox.com/v1/games?universeIds={UID}").json()["data"][0]["creator"]["name"]

while True:
    if IsProgramOpen(RobloxProcName):
        break

    time.sleep(1)

StartTime = time.time()

RPC.connect()

print("LatteJuice connected to Discord RPC. Do not close the terminal if you want to keep it connected. LatteJuice will auto close when roblox is closed.")

while IsProgramOpen(RobloxProcName):
    RPC.update(
        details=GAMENAME,
        state=f"by {GAMECREATOR}",
        large_image=GAMETHUMBNAIL,
        small_image="lattejuice",
        large_text="Powered by LatteJuice.",
        start=StartTime + 3,
        buttons=[
                {
                    "label": "See Details",
                    "url": f"https://www.roblox.com/games/{gameid}",
                },
            ],
    )
    time.sleep(1)