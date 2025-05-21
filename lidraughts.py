import os, re, aiohttp, asyncio, json
from dotenv import load_dotenv
import requests

load_dotenv()
TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    print("Please set a TOKEN")
    exit()
headers = {"Authorization": f"Bearer {TOKEN}"}

event_stack = []

def is_bot_account() -> bool:
    url = "https://lidraughts.org/api/account"

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print(r.reason)
        exit(1)

    return r.json().get("title") == "BOT"

def upgrade_to_bot_account():
    url = "https://lidraughts.org/api/bot/account/upgrade"

    r = requests.post(url, headers=headers)

    if r.status_code != 200:
        print(r.reason)
        exit(1)

async def get_incoming_events_from_stream():
    url = "https://lidraughts.org/api/stream/event"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            buf = ''
            async for chunk in response.content.iter_any():
                buf += chunk.decode('utf-8')
                buf = re.sub(r"^ *\n", "", buf)
                if not buf:
                    continue

                for line in buf.split("\n"):
                    if not line:
                        continue
                    event_stack.append(line)
                buf = ""

async def treat_events():
    while True:
        await asyncio.sleep(0.25)
        while event_stack:
            event = event_stack.pop()
            event = json.loads(event)
            event_type = event.get("type")
            if event_type == "challenge":
                challenge_id = event["challenge"]["id"]
                url = f"https://lidraughts.org/api/challenge/{challenge_id}/accept"
                print("challenge_id", challenge_id)
                requests.post(url, headers=headers)
            elif event_type == "gameStart":
                game_id = event["game"]["id"]
                url = f"https://lidraughts.org/api/bot/game/{game_id}/abort"
                print("game_id", game_id)
                requests.post(url, headers=headers)
            else:
                print(event)


async def main():
    # ensure that we have a bot account
    if not is_bot_account():
        print("upgrading to bot account...")
        upgrade_to_bot_account()
        print("upgraded to bot account")
    else:
        print("already a bot account")

    await asyncio.gather(
        get_incoming_events_from_stream(),
        treat_events()
    )

if __name__ == "__main__":
    asyncio.run(main())
