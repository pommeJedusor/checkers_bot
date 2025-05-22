import os, re, aiohttp, asyncio, json
from dotenv import load_dotenv
import requests

from Checkers import Checkers
from Minimax import minimax
import PDN
from consts import Player

load_dotenv()
TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    print("Please set a TOKEN")
    exit()
headers = {"Authorization": f"Bearer {TOKEN}"}

event_stack = []

profile_id = None


def get_profile_id() -> str:
    url = "https://lidraughts.org/api/account"
    return profile_id or requests.get(url, headers=headers).json()["id"]


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
            buf = ""
            async for chunk in response.content.iter_any():
                buf += chunk.decode("utf-8")
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
                # url = f"https://lidraughts.org/api/bot/game/{game_id}/abort"
                # print("game_id", game_id)
                # requests.post(url, headers=headers)
                asyncio.create_task(get_incoming_events_from_game_stream(game_id))
            else:
                print(event)


async def get_incoming_events_from_game_stream(game_id):
    url = f"https://lidraughts.org/api/bot/game/stream/{game_id}"
    board = Checkers()
    board.init_board()
    color = None
    moves = []
    constructed_move = ""

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                buf = ""
                async for chunk in response.content.iter_any():
                    buf += chunk.decode("utf-8")
                    buf = re.sub(r"^ *\n", "", buf)
                    if not buf:
                        continue

                    for line in buf.split("\n"):
                        if not line:
                            continue
                        data = json.loads(line)
                        event_type = data.get("type")
                        print(game_id, line)
                        if event_type == "chatLine":
                            continue
                        elif event_type == "gameState":
                            moves = data.get("moves").split(" ")
                            move = moves[-1]
                            print("move:", moves[-1])
                            if len(moves[-1]) > 4:
                                constructed_move += moves[-1][:2]
                                print("constructed_move", constructed_move)
                                continue
                            elif len(moves[-1]) == 4 and constructed_move:
                                constructed_move += moves[-1]
                                print("constructed_move", constructed_move)
                                move = constructed_move
                                constructed_move = ""
                            try:
                                PDN.make_lidraughts_move(board, move)
                            except Exception as e:
                                print("move failed")
                                print(e)
                                continue
                            # board.show_board()

                        elif event_type == "gameFull":
                            white_player_id = data["white"]["id"]
                            if white_player_id == get_profile_id():
                                color = Player.WHITE
                            else:
                                color = Player.BLACK

                        if (
                            color == Player.WHITE
                            and len(board.moves) % 2 == 1
                            or color == Player.BLACK
                            and len(board.moves) % 2 == 0
                        ):
                            continue

                        # if lost
                        if not board.get_moves():
                            return

                        move, score = minimax(board)
                        if not move:
                            print("Error: move not found")
                            return
                        # board.show_board()
                        print("I play:", PDN.get_lidraughts_move_notation_list(move))
                        for move in PDN.get_lidraughts_move_notation_list(move):
                            url = f"https://lidraughts.org/api/bot/game/{game_id}/move/{move}"
                            r = requests.post(url, headers=headers)
                            if json.loads(r.content).get("error"):
                                print(json.loads(r.content).get("error"))
                    buf = ""
    except Exception as e:
        print(e)


async def main():
    # ensure that we have a bot account
    if not is_bot_account():
        print("upgrading to bot account...")
        upgrade_to_bot_account()
        print("upgraded to bot account")
    else:
        print("already a bot account")

    await asyncio.gather(get_incoming_events_from_stream(), treat_events())


if __name__ == "__main__":
    asyncio.run(main())
