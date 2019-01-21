import json
import os
from urllib.parse import urlencode
from urllib.request import urlopen

try:
    from algoliasearch import algoliasearch
except ImportError:
    print("Algolia Search package does not exist - pip install algoliasearch")

try:
    import toml
except ImportError:
    print("TOML package does not exist - pip install toml")

# ------- Algolia Start ---------

APP_ID = "UT1XVMZE1Q"
INDEX_NAME = "gollahalli-website"
file_path = os.path.join('public', 'searchindex.json')

client = algoliasearch.Client(APP_ID, os.environ.get('ALGOLIA_KEY'))
index = client.init_index(INDEX_NAME)

index.clear_index()  # Clear previous entries.

batch = json.load(open(file_path))
index.add_objects(batch)
print("Successfully uploaded index to Algolia.")

# ------- Algolia End ---------

# ------- Sitemap Ping Start ---------
GOOGLE_PING_URL = "https://www.google.com/webmasters/tools/ping"
BING_PING_URL = "https://www.bing.com/ping?sitemap"

config = toml.load("./config.toml")

params = urlencode({'sitemap': config["baseURL"] + "sitemap.xml"})
print("Pinging Google")
urlopen('%s?%s' % (GOOGLE_PING_URL, params))
print("Pinging Bing")
urlopen('%s?%s' % (BING_PING_URL, params))

print("Done!")

# ------- Sitemap Ping End ---------
