# Motivation

There doesn't seem to be an easy to assess the "Slack Age" of someone i.e.
when they joined. This tries to approximate this based on what is
available.

I may have missed some better way to do this, so please ping me if there
is an obvious way to do this.

# Prerequisites

* python3, virtualenv, pip
* a slack api token (API_TOKEN below)
    * see https://api.slack.com/bot-users, specifically https://my.slack.com/services/new/bot

# Install

    virtualenv venv
    source ./venv/bin/activate

    pip3 install -r requirements.txt

# Usage

## Setup defaults

    export API_TOKEN="your-api-token"

## Crawl

Find first 2000 members that look like real people, and use their
first reaction to a message as a proxy for when they joined.

    python3 crawl.py --token $API_TOKEN --limit 2000
