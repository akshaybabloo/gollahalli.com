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

app_id = "UT1XVMZE1Q"
index_name = "gollahalli-website"
file_path = os.path.join('public', 'searchindex.json')

client = algoliasearch.Client(app_id, os.environ.get('ALGOLIA_KEY'))
index = client.init_index(index_name)

batch = json.load(open(file_path))
index.add_objects(batch)
print("Successfully uploaded index to Algolia.")

# ------- Algolia End ---------

# ------- Google Ping Start ---------

PING_URL = "https://www.google.com/webmasters/tools/ping"

config = toml.load("./config.toml")

params = urlencode({'sitemap': config["baseURL"] + "sitemap.xml"})
urlopen('%s?%s' % (PING_URL, params))

# ------- Google Ping End ---------
