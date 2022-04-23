# Requirements
* Python 3.7+
* pip installed

# Install
> pip install -r requirements.txt

# Running
First edit tezos.raffles.py constants you need at the top.

```python
CONTRACT = "KT1H436mFXZ1KqCVDUv2YQ23RnqMYKThhqah"
LEDGER_PATH="assets.ledger"
TZXT_API = "https://api.tzkt.io/v1"

# Needs to be in ISO format, so May 9th 1980 at 2:00 and 31 seconds is 1980-05-09T02:00:31+00Z
# You may set this to None to pick the most recent time on the network
DATE_TO_SNAPSHOT="2022-04-23T02:00:31+00Z"
#NUM_OF_WINNERS is the number of winners you want to pick, a winner has equal chance of being picked each NUM times
NUM_OF_WINNERS=100
# WAIT_LEVELS is how many blocks on tezos to wait from the start of running this program to get the hash
# for the random seeders.  This helps earn trust that the selection is random and it is not feasiable to have
# ran this program multiple times to force a winner
WAIT_LEVELS = 1
#VERIFY_LEVEL if not None, specifies the level which the raffle was originally ran on and you can set this
#to verify/get the same results as when this was ran
VERIFY_LEVEL = None

```
> python tezos_raffles

# Limitations
Currently, the code only supports up to 10000 total holders at any time. If you need more file an issue.

# If you like this....
Drop a few tez my way on Tezos to show your appreciate and motivate me to keep creating and publicly releasing scripts and tools for tezos.
`tacoby.tez tz1aJznwEALEC6WpLaRspXCm7YyATxdNftVg`