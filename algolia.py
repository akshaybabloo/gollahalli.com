from algoliasearch import algoliasearch
import os
import json

client = algoliasearch.Client("UT1XVMZE1Q", os.environ.get('ALGOLIA_KEY'))
index = client.init_index('gollahalli-website')

batch = json.load(open(os.path.join('public', 'searchindex.json')))
index.add_objects(batch)
