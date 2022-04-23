import datetime
import random
from collections import defaultdict
from random import choices
from time import sleep

import requests
from pytz import UTC

CONTRACT = "KT1H436mFXZ1KqCVDUv2YQ23RnqMYKThhqah"
LEDGER_PATH = "assets.ledger"
TZKT_API = "https://api.tzkt.io/v1"

# Needs to be in ISO format, so May 9th 1980 at 2:00 and 31 seconds is 1980-05-09T02:00:31+00Z
# You may set this to None to pick the most recent time on the network
DATE_TO_SNAPSHOT = "2022-04-23T02:00:31+00Z"
# NUM_OF_WINNERS is the number of winners you want to pick, a winner has equal chance of being picked each NUM times
NUM_OF_WINNERS = 100
# WAIT_LEVELS is how many blocks on tezos to wait from the start of running this program to get the hash
# for the random seeders.  This helps earn trust that the selection is random and it is not feasiable to have
# ran this program multiple times to force a winner
WAIT_LEVELS = 1
# VERIFY_LEVEL if not None, specifies the level which the raffle was originally ran on and you can set this
# to verify/get the same results as when this was ran
VERIFY_LEVEL = None


def pick_winners(addresses, hash, weights):
    random.seed(hash)
    winners = choices(addresses, weights, k=NUM_OF_WINNERS)
    return winners


def wait_for_level_and_get_seed(sess, level):
    while True:
        resp = sess.get(TZKT_API + f"/blocks/{level + WAIT_LEVELS}")
        if resp.status_code != 200:
            print('.', end='')
            sleep(10)
            continue
        break
    hash, level, timestamp = resp.json()['hash'], resp.json()['level'], resp.json()['timestamp']
    print(f"\nfound level on chain is {level} at {timestamp} with {hash}")
    return hash


def get_holders(sess):
    resp = sess.get(TZKT_API + "/statistics",
                    params={"timestamp.le": DATE_TO_SNAPSHOT, "sort.desc": "level", "limit": 1})
    level_at_requested_time = resp.json()[0]['level']
    latest_time_at_requested_time = resp.json()[0]['timestamp']
    print(
        f"Gathering owners at {DATE_TO_SNAPSHOT} from block level {level_at_requested_time} at {latest_time_at_requested_time}")
    resp = sess.get(TZKT_API + f"/contracts/{CONTRACT}/bigmaps/{LEDGER_PATH}/historical_keys/{level_at_requested_time}",
                    params={"limit": 10000, "value.ne": "0"})
    entries = defaultdict(int)
    total = 0
    for token in resp.json():
        entries[token["key"]["address"]] += int(token["value"])
        total += int(token["value"])
        # print(f'id: {token["key"]["nat"]} owner:{token["key"]["address"]} amount:{token["value"]}')
    addresses = []
    weights = []
    for address, amount in entries.items():
        print(f'{address} has {amount} entries')
        addresses.append(address)
        weights.append(amount / total)
    return addresses, entries, weights


def run_raffle():
    start_time = datetime.datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S+00Z")
    results_file = f'results-{CONTRACT}-{datetime.datetime.now(UTC).strftime("%m-%d-%Y_%H-%M-%S")}.txt'
    with requests.session() as sess:

        print("Generating hash from blockchain data.")
        if VERIFY_LEVEL is None:
            level = get_current_level(sess)
        else:
            level = VERIFY_LEVEL
        hash = wait_for_level_and_get_seed(sess, level)
        print(f"Getting list of holders at {DATE_TO_SNAPSHOT}")
        addresses, entries, weights = get_holders(sess)
        winners = pick_winners(addresses, hash, weights)
        with open(results_file, "wt") as f:

            line = f"Winner results for holders on {DATE_TO_SNAPSHOT} ran at {start_time} "
            print(line)
            print(line, file=f)
            for i, winner in enumerate(winners, start=1):
                line = f"{i}. winner is {winner} they had {entries[winner]} entries!"
                print(line)
                print(line, file=f)
            line = f"You can verify this raffle with VERIFY_LEVEL={level} NUM_OF_WINNER={NUM_OF_WINNERS}"
            print(line)
            print(line, file=f)


def get_current_level(sess):
    resp = sess.get(TZKT_API + "/head")
    hash, level, timestamp = resp.json()['hash'], resp.json()['level'], resp.json()['timestamp']
    print(f"current level on chain is {level} at {timestamp} with {hash}, waiting for {level + WAIT_LEVELS}")
    return level


run_raffle()
