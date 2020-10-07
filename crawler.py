#!/usr/bin/env python3

from helpers import api

all_papers = api.get_all_papers()
print(f"Loaded {len(all_papers)} papers")

conflicts = api.get_conflicts()

print("Found conflicts:")
for i, c in enumerate(conflicts):
    print(f"  {i}: {all_papers[c]['content']['title']}")

excluded = conflicts

n = 0
def write_paper(paper_id, f, score = None):
    global n
    if paper_id in excluded:
        return
    excluded.add(paper_id)
    n+=1

    paper = all_papers[paper_id]
    content = paper['content']
    f.write("------------------------------------------------------------------\n")
    f.write(f"{paper['number']}: {content['title']}\n")
    f.write("\n")
    if  content.get('keywords') :
        f.write(f"Keywords: {','.join(content['keywords'])}\n")
    if "one-sentence_summary" in content:
        f.write(f"Summary: {content['one-sentence_summary']}\n")
    if "forum" in paper:
        f.write(f"URL: https://openreview.net/forum?id={paper['forum']}\n")

    if score is not None:
        f.write(f"Score: {score}\n")
    f.write("\n")
    f.write(content["abstract"])
    f.write("\n\n")

scores = api.get_affinity()

missing = [pd["head"] for pd in scores if pd["head"] not in all_papers]
print(f"Missing {len(missing)} papers")


with open('output.txt', 'w') as f:
    for pd in scores:
        if pd["head"] not in all_papers:
            print(f"  Found recommended withdrawn paper: {pd['head']}")
            continue
        write_paper(pd["head"], f, pd["weight"])

    for id in all_papers.keys():
        write_paper(id, f)
