"""
Utility for deploying https://www.gollahalli.com
"""
import json
import os
from urllib.parse import urlencode
from urllib.request import urlopen
from colorama import init, Fore, Style

try:
    from algoliasearch.search_client import SearchClient
except ImportError:
    raise ImportError("PY> Algolia Search package does not exist - pip install algoliasearch")

try:
    import toml
except ImportError:
    raise ImportError("PY> TOML package does not exist - pip install toml")


# ------------------ End Hashing Files ------------------


def colour_me(text: str) -> str:
    """
    Returns a dark green text
    """
    init(autoreset=True)

    return Style.BRIGHT + Fore.GREEN + text


# ------- Algolia Start ---------

APP_ID = "UT1XVMZE1Q"
INDEX_NAME = "gollahalli-website"
FILE_PATH = os.path.join('public', 'searchindex.json')

CLIENT = SearchClient.create(APP_ID, os.environ.get('ALGOLIA_KEY'))
INDEX = CLIENT.init_index(INDEX_NAME)

print(colour_me("PY> Clearing Previous Search Entries..."), end='')
INDEX.clear_objects()  # Clear previous entries.
print(colour_me("Done"))

print(colour_me("PY> Uploading New Search Index..."), end='')
BATCH = json.load(open(FILE_PATH))
INDEX.save_objects(BATCH)
print(colour_me("Done"))

# ------- Algolia End ---------

# ------- Sitemap Ping Start ---------
GOOGLE_PING_URL = "https://www.google.com/webmasters/tools/ping"
BING_PING_URL = "https://www.bing.com/ping?sitemap"

CONFIG = toml.load("./config.toml")

# PARAMS = urlencode({'sitemap': CONFIG["baseURL"] + "sitemap.xml"})
# print(colour_me("PY> Pinging Google..."), end='')
# urlopen('%s?%s' % (GOOGLE_PING_URL, PARAMS))
# print(colour_me("Done"))
# print(colour_me("PY> Pinging Bing..."), end='')
# urlopen('%s?%s' % (BING_PING_URL, PARAMS))
# print(colour_me("Done"))

print(colour_me("PY> Content deployed at"), colour_me(CONFIG["baseURL"]))

# ------- Sitemap Ping End ---------
