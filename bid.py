#!/usr/bin/env python3

from helpers.config import config, cookie
from helpers import api
import urllib.parse
import requests
import json
from tqdm import tqdm


def load_votes():
    with open("votes.txt") as v:
        votes = v.readlines()

    votes=[v.split("#")[0].strip() for v in votes]
    votes = ",".join(votes)
    votes=[v.strip() for v in votes.split(",")]

    eager = set([int(v[:-1].strip()) for v in votes if v.endswith("*")])
    rest = set([v2 for v2 in [int(v.strip()) for v in votes if not v.endswith("*")] if v2 not in eager])

    print(f"Total number of papers: {len(eager) + len(rest)}")

    print(f"eager = {list(eager)};")
    print(f"rest = {list(rest)};")
    return set(eager), set(rest)

eager, non_eager = load_votes()

all_papers = api.get_all_papers()
num_to_paper = {p["number"]: p for p in all_papers.values()}

print(f"Loaded {len(all_papers)} papers")

bidded = api.get_bidded()
print(f"Current number of bids: {len(bidded)}")
for i, b in enumerate(bidded.keys()):
    print(f"   {i}: {all_papers[b]['content']['title']} - {bidded[b]['label']}")

print("Current bid descriptor: ", ",".join([str(all_papers[pid]['number']) + ('*' if b['label'] == 'Very High' else '') for pid, b in bidded.items()]))


print("Removing current bids")
for i,b in enumerate(tqdm(bidded.keys())):
    api.bid(bidded[b]["id"], b, bidded[b]['label'], True)

print("Bidding...")
for id in tqdm(list(eager) + list(non_eager)):
    paper = num_to_paper[id]
    label = 'Very High' if id in eager else 'High'
    api.bid(None, paper["id"], label, False)

print("Done")



#
# bids = get_bidded()
# print(bids)

#payload = '{"id":null,"invitation":"ICLR.cc/2021/Conference/Reviewers/-/Bid","label":"Very High","head":"V4AVDoFtVM","tail":"~Jürgen_Schmidhuber1","signatures":["~Jürgen_Schmidhuber1"],"writers":["~Jürgen_Schmidhuber1"],"readers":["ICLR.cc/2021/Conference","ICLR.cc/2021/Conference/Area_Chairs","~Jürgen_Schmidhuber1"],"nonreaders":["ICLR.cc/2021/Conference/Paper1640/Authors"],"ddate":null}'
#payload = '{"id":"iXli1jC8oV","invitation":"ICLR.cc/2021/Conference/Reviewers/-/Bid","label":"Very High","head":"V4AVDoFtVM","tail":"~Jürgen_Schmidhuber1","signatures":["~Jürgen_Schmidhuber1"],"writers":["~Jürgen_Schmidhuber1"],"readers":["ICLR.cc/2021/Conference","ICLR.cc/2021/Conference/Area_Chairs","~Jürgen_Schmidhuber1"],"nonreaders":["ICLR.cc/2021/Conference/Paper1640/Authors"],"ddate":null}'
#h = {"content-type": "application/json"}
#h.update(cookie)
#data = requests.post("https://api.openreview.net/edges", payload.encode(), headers = cookie)
#print(data.headers)
#print(data.content.decode())


#"https://api.openreview.net/notes/search"