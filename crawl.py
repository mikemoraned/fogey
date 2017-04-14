import logging
from optparse import OptionParser
from slacker import Slacker

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)

parser = OptionParser()
parser.add_option("-t", "--token", dest="token", help="your slack token")

(options, args) = parser.parse_args()

slack = Slacker(options.token)


def extract_oldest_timestamp(current, reactions):
    oldest_ts = current
    for item in reactions.body["items"]:
        if "message" in item:
            message = item["message"]
            if "ts" in message:
                oldest_ts = message["ts"]
    return oldest_ts


def oldest_reaction(user_id):
    reactions = slack.reactions.list(user_id)
    oldest_ts = extract_oldest_timestamp(None, reactions)
    paging = reactions.body["paging"]
    pages = paging["pages"]
    if pages > 1:
        for page in range(2, pages):
            oldest_ts = extract_oldest_timestamp(
                oldest_ts,
                slack.reactions.list(user_id, page=page))
    return oldest_ts

response = slack.users.list()
for member in response.body["members"]:
    if not member['deleted'] and not member['is_bot']:
        print(member)
        oldest_ts = oldest_reaction(member["id"])
        print(oldest_ts)
