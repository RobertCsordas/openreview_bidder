# OpenReview paper bidding tool

## What is it good for?

If you want to distribute the paper reviews in your team, you also might want people from the team to bid for the papers. But bidding requires to be logged in with your account.

This tool enables to download the list of titles and abstracts, send that to people, collect their responses and upload the bids automatically.

## How to use it?

1) Log in to OpenReview. Extract cookie ```openreview.accessToken``` from the browser debug console (needed for the session). You can do this by inspecting the header of any request.
2) Create ```config.json``` with cookie and conference name (see template below)
3) Run ```craweler.py```. This will create ```output.txt``` which is a readable format with paper ordered by their relevance score. Send this to your collegues.
4) Collect the votes of your collegues in a format of comma delimited ID lists, with stars after the "Very High" votes. The rest of them will be "High". An example list looks like "34,56*,1235*,64". You can use comments on end of line, separated by hashmark
5) Paste all the ID lists in ```votes.txt``` (you can use spaces and newlines after commas)
6) Run bid.py

## Example "config.json"

```json
{
    "invitation_id": "ICLR.cc/2021/Conference/Reviewers/-/Bid",
    "session_id": "some_huge_string"
}
```

## Example "votes.txt"

```
294*,432*,3901,5477*,5593*,6986 # From user1
124*,589*,968*,136,3897 # Random comment
```