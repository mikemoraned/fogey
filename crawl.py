import logging
from collections import defaultdict
from optparse import OptionParser
from slacker import Slacker
import datetime
import re

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)

parser = OptionParser()
parser.add_option("-t", "--token", dest="token",
                  help="your slack token")
parser.add_option("-l", "--limit", type=int, dest="max_members",
                  help="maximum number of members")

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


grouped_by_month = defaultdict(list)
response = slack.users.list()
max_members = options.max_members
members = 0
for member in response.body["members"]:
    if not member['deleted'] \
            and not member['is_bot'] \
            and members < max_members:
        members += 1
        print(member)
        oldest_ts = oldest_reaction(member["id"])
        if oldest_ts:
            oldest_datetime = datetime.datetime.fromtimestamp(
                int(re.sub("\..+", "", oldest_ts)))
            oldest_month = oldest_datetime.strftime("%Y-%m")
            grouped_by_month[oldest_month].append(
                (member["id"], member["name"]))

months = sorted(grouped_by_month.keys())
for month in months:
    members = grouped_by_month[month]
    print("{}: {}, {}".format(month, len(members), members))
