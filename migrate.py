import os.path
import threading
import traceback

import bigjson
import humanfriendly
import psycopg2
import requests
from dotenv import load_dotenv

load_dotenv()
import os

dest = "https://tetrio.team2xh.net/data/player_history.js"
out = "history.json"


def download(url: str):
    response = requests.get(url, stream=True)
    print(f"Downloading {url}")
    with open(out, "wb") as f:
        dl = 0
        for data in response.iter_content(chunk_size=1024):
            dl += len(data)
            print(f"Writing {humanfriendly.format_size(dl)}        []", end="\r")
            f.write(data)


if not os.path.exists(out):
    download(dest)

with open(out, "rb") as f:
    print("loading json")
    data: bigjson = bigjson.load(f)
    print("loaded json")
    a = psycopg2.connect(
        f"dbname='{os.getenv('DB_DATABASE')}' user='{os.getenv('DB_USERNAME')}' host='{os.getenv('DB_HOST')}' password='{os.getenv('DB_PASSWORD')}'"
    )
    print("connected to database")
    a.cursor().execute(
        "CREATE TABLE IF NOT EXISTS player_history(name TEXT, rank TEXT, tr BIGINT);"
    )
    print("created table")

    def put_player_infos_to_db(player_name: str, rank: str, tr: int) -> None:
        c = a.cursor()
        try:
            c.execute(
                "INSERT INTO player_history VALUES (%s, %s, %s);",
                (player_name, rank, tr),
            )
        except Exception as e:
            traceback.print_exc()
            exit()
        c.close()
        print("added player", player_name, rank, tr)

    t = []
    for player, data in data["ranks"].items():
        k = threading.Thread(
            target=put_player_infos_to_db, args=(player, data["rank"][0], data["tr"][0])
        )
        k.daemon = True
        k.start()
        t.append(k)

    for thread in t:
        thread.join()

    a.commit()
