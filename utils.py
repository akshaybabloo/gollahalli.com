import hashlib
import json
import os
from urllib.parse import urlencode
from urllib.request import urlopen

try:
    from algoliasearch import algoliasearch
except ImportError:
    raise ImportError("PY> Algolia Search package does not exist - pip install algoliasearch")

try:
    import toml
except ImportError:
    raise ImportError("PY> TOML package does not exist - pip install toml")

CDGREEN = '\33[92m'
CBOLD = '\033[1m'
CEND = '\033[0m'

# ------------------ Start Hashing Files ------------------

here = os.path.abspath(os.path.dirname(__file__)) + os.sep

BUF_SIZE = 65563

dependencies = {
    "node_modules": {
        "instantsearch.js": [
            os.path.join('dist', 'instantsearch.development.js')
        ],
        "algoliasearch": [
            os.path.join('dist', 'algoliasearchLite.js')
        ],
        "uikit": [
            os.path.join('dist', 'css', 'uikit.css'),
            os.path.join('dist', 'js', 'uikit.js'),
            os.path.join('dist', 'js', 'uikit-core.js')
        ]
    }
}

hashed_files = {}

sha256 = hashlib.sha256()

for root_folder, sub_folder in dependencies.items():
    for sub_sub_folder, files_list in sub_folder.items():
        for file in files_list:
            file_path = os.path.join(root_folder, sub_sub_folder, file)
            with open(file_path, 'rb') as byte_file:
                data = byte_file.read()
                sha256.update(data)
                hashed_files.update({'{}'.format(file_path): '{}'.format(sha256.hexdigest())})
import pprint

pprint.pprint(hashed_files)


# ------------------ End Hashing Files ------------------


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

print(colour_me("PY> Clearing Previous Search Entries..."), end='')
index.clear_index()  # Clear previous entries.
print(colour_me("Done"))

print(colour_me("PY> Uploading New Search Index..."), end='')
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

print(colour_me("PY> Content deployed at"), colour_me(config["baseURL"]))

# ------- Sitemap Ping End ---------
