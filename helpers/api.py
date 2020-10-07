from .config import config, cookie, conference_base
import requests
import json
from functools import lru_cache
from lxml import html
from datetime import datetime


@lru_cache
def get_username():
    main_page = requests.get("https://openreview.net/invitation?id="+config["invitation_id"], headers = cookie)
    tree = html.fromstring(main_page.content.decode())
    data_block = tree.xpath("//script[@id='__NEXT_DATA__']")
    assert len(data_block) == 1
    data_block = data_block[0]


    data_block = data_block.text
    user_block_start = "\\\"usernames\\\":["
    user_pos = data_block.find(user_block_start)
    assert user_pos > 0
    user_pos += len(user_block_start)
    user_end_pos = data_block.find("]", user_pos+1)
    user_list = data_block[user_pos:user_end_pos].split(",")
    assert len(user_list) == 1
    return user_list[0].strip()[2:-2]


def get_affinity():
    user = get_username()

    l = requests.get("https://api.openreview.net/edges", headers = cookie, params={
        "invitation": config["invitation_id"][:-3]+"Affinity_Score",
        "tail": user,
        "sort": "weight:desc",
    })

    paper_ids = json.loads(l.content.decode())
    return paper_ids["edges"]

def get_conflicts():
    user = get_username()

    l = requests.get("https://api.openreview.net/edges", headers=cookie, params={
        "invitation": config["invitation_id"][:-3] + "Conflict",
        "tail": user
    })

    return set(a["head"] for a in json.loads(l.content.decode())["edges"])

@lru_cache
def get_all_papers():
    offset = 0
    count = 10000
    notes = []

    while offset < count:
        print(f"Downloading papers from offset {offset}")
        data = requests.get("https://api.openreview.net/notes", headers=cookie, params={
            "invitation": "/".join(config["invitation_id"].split("/")[:3]+["-","Blind_Submission"]),
            "offset": offset,
            "count": 1000
        })

        data = json.loads(data.content.decode())
        offset += len(data["notes"])
        count = data["count"]
        notes = notes + data["notes"]

    notes = {n["id"]: n for n in notes}
    return notes


def get_bidded():
    user = get_username()

    l = requests.get("https://api.openreview.net/edges", headers = cookie, params={
        "invitation": config["invitation_id"],
        "tail": user,
    })

    bidded = json.loads(l.content.decode())["edges"]
    return {b['head']: b for b in bidded}

def get_author_ids(paper_id):
    all_papers = get_all_papers()
    return all_papers[paper_id]["content"]["authorids"]

def bid(bid_id, paper_id, label, delete):
    user = get_username()
    payload = {
        "id": bid_id,
        "invitation": config["invitation_id"],
        "label": label,
        "head": paper_id,
        "tail": user,
        "signatures": [
            user
        ],
        "writers": [
            user
        ],
        "readers": [
            conference_base,
            f"{conference_base}/Area_Chairs",
            user
        ],
        "nonreaders": get_author_ids(paper_id),
        "ddate": int(datetime.utcnow().timestamp()*1000) if delete else None
    }

    payload = json.dumps(payload, ensure_ascii=False, separators=(',', ':'))
    res = requests.post("https://api.openreview.net/edges", payload.encode(), headers=cookie)
    res = res.content.decode()
    if delete:
        return None
    else:
        return json.loads(res)
