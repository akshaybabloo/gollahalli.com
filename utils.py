import json
import os
from urllib.parse import urlencode
from urllib.request import urlopen

try:
    from algoliasearch import algoliasearch
except ImportError:
    print("PY> Algolia Search package does not exist - pip install algoliasearch")

try:
    import toml
except ImportError:
    print("PY> TOML package does not exist - pip install toml")

CDGREEN = '\33[92m'
CBOLD = '\033[1m'
CEND = '\033[0m'

def colour_me(text: str) -> str:
    """
    Returns a dark green text
    """
    return CBOLD + CDGREEN + text + CEND

# ------- Algolia Start ---------

APP_ID = "UT1XVMZE1Q"
INDEX_NAME = "gollahalli-website"
file_path = os.path.join('public', 'searchindex.json')

client = algoliasearch.Client(APP_ID, os.environ.get('ALGOLIA_KEY'))
index = client.init_index(INDEX_NAME)

print(colour_me("PY> Clearing Previous Entries..."), end='')
index.clear_index()  # Clear previous entries.
print(colour_me("Done"))

print(colour_me("PY> Uploading New Index..."), end='')
batch = json.load(open(file_path))
index.add_objects(batch)
print(colour_me("Done"))

# ------- Algolia End ---------

# ------- Sitemap Ping Start ---------
GOOGLE_PING_URL = "https://www.google.com/webmasters/tools/ping"
BING_PING_URL = "https://www.bing.com/ping?sitemap"

config = toml.load("./config.toml")

params = urlencode({'sitemap': config["baseURL"] + "sitemap.xml"})
print(colour_me("PY> Pinging Google..."), end='')
urlopen('%s?%s' % (GOOGLE_PING_URL, params))
print(colour_me("Done"))
print(colour_me("PY> Pinging Bing..."), end='')
urlopen('%s?%s' % (BING_PING_URL, params))
print(colour_me("Done"))

print(colour_me("PY> Content deployed at "), colour_me(config["baseURL"]))

# ------- Sitemap Ping End ---------
