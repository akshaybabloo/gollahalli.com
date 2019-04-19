import hashlib
import json
import os
from urllib.parse import urlencode
from urllib.request import urlopen


try:
    from pathlib import Path
except ImportError:
    raise ImportError("PY> Works on Python 3.5 and above only")

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
            os.path.join('dist', 'js', 'uikit-icons.js')
        ]
    }
}

copy_file_to = {
    'instantsearch.development.js': os.path.join(here, 'themes', 'Spark', 'assets', 'js'),
    'algoliasearchLite.js': os.path.join(here, 'themes', 'Spark', 'assets', 'js'),
    'uikit.css': os.path.join(here, 'themes', 'Spark', 'assets', 'css'),
    'uikit.js': os.path.join(here, 'themes', 'Spark', 'assets', 'js'),
    'uikit-icons.js': os.path.join(here, 'themes', 'Spark', 'assets', 'js'),
}


def get_lock_dict(dependency: dict) -> dict:
    """
    Creates a hash for every file path.

    :param dependency: Dictionary of file location
    :rtype: dict
    :return: A dictionary of file path and it's SHA512 hash

    >>> dependencies = {
            "node_modules": {
                "instantsearch.js": [
                    os.path.join('dist', 'instantsearch.development.js')
                ]
            }
    >>> get_lock_dict(dependencies)
    {
        "node_modules/instantsearch.js/dist/instantsearch.development.js": "sha512-d71f0cf0b5138d86dd32096bd1f4b449f3e70ace6c207757859f1165559b82e47c95a527b075153b4cf89450eb5369b8c73afd4013e6336e195f79fde2d0bca2"
    }
    """
    lock_dict = {}
    sha256 = hashlib.sha512()

    for root_folder, sub_folder in dependency.items():
        for sub_sub_folder, files_list in sub_folder.items():
            for file in files_list:
                file_path = os.path.join(root_folder, sub_sub_folder, file)
                with open(file_path, 'rb') as byte_file:
                    data = byte_file.read()
                    sha256.update(data)
                    lock_dict.update({'{}'.format(file_path): 'sha512-{}'.format(sha256.hexdigest())})

    return lock_dict


def compare_hash(lock_dict: dict, dependency: dict):
    pass


if Path(os.path.join(here, 'gollahalli.lock')).is_file():
    lock_file = json.load(open('gollahalli.lock'))

    compare_hash(lock_file, get_lock_dict(dependencies))
else:
    hash_dict = get_lock_dict(dependencies)
    with open('gollahalli.lock', 'w') as hashed:
        json.dump(hash_dict, hashed, indent=4)


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
