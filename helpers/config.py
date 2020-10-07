import json


with open("config.json") as f:
    config = json.load(f)

cookie = {
     'Content-Type': 'application/json; charset=UTF-8',
     'cookie': "openreview.accessToken="+config["session_id"]
}

conference_base = "/".join(config["invitation_id"].split("/")[:3])
