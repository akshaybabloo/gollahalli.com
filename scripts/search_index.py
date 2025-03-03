"""
Utility for deploying https://www.gollahalli.com
"""
import json
import os
from urllib.parse import urlencode
from urllib.request import urlopen
from rich.console import Console

try:
    from algoliasearch.search.client import SearchClientSync as SearchClient
except ImportError:
    raise ImportError("PY> Algolia Search package does not exist - pip install algoliasearch")

try:
    import toml
except ImportError:
    raise ImportError("PY> TOML package does not exist - pip install toml")


# ------------------ End Hashing Files ------------------

con = Console()

# ------- Algolia Start ---------

APP_ID = "UT1XVMZE1Q"
INDEX_NAME = "gollahalli-website"
FILE_PATH = os.path.join('public', 'searchindex.json')

CLIENT = SearchClient(APP_ID, os.environ.get('ALGOLIA_KEY'))
INDEX = CLIENT.search_single_index(INDEX_NAME)

con.print("PY> Clearing Previous Search Entries...", end='', style="bold green")
CLIENT.clear_objects(INDEX_NAME)  # Clear previous entries.
con.print("Done", style="bold green")

con.print("PY> Uploading New Search Index...", end='', style="bold green")
BATCH = json.load(open(FILE_PATH))
CLIENT.save_objects(INDEX_NAME, BATCH, wait_for_tasks=True)
con.print("Done", style="bold green")

# ------- Algolia End ---------

# ------- Sitemap Ping Start ---------
GOOGLE_PING_URL = "https://www.google.com/webmasters/tools/ping"
BING_PING_URL = "https://www.bing.com/ping?sitemap"

CONFIG = toml.load("./config.toml")

# PARAMS = urlencode({'sitemap': CONFIG["baseURL"] + "sitemap.xml"})
# con.print("PY> Pinging Google...", end='', style="bold green")
# urlopen('%s?%s' % (GOOGLE_PING_URL, PARAMS))
# con.print("Done", style="bold green")
# con.print("PY> Pinging Bing...", end='', style="bold green")
# urlopen('%s?%s' % (BING_PING_URL, PARAMS))
# con.print("Done", style="bold green")

con.print(f"PY> Content deployed at: {CONFIG['baseURL']}", style="bold green")

# ------- Sitemap Ping End ---------
