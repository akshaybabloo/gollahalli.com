from algoliasearch import algoliasearch
import os
import json

app_id = "UT1XVMZE1Q"
index_name = "gollahalli-website"
file_path = os.path.join('public', 'searchindex.json')

client = algoliasearch.Client(app_id, os.environ.get('ALGOLIA_KEY'))
index = client.init_index(index_name)

batch = json.load(open(file_path))
index.add_objects(batch)
print("Successfully uploaded index to Algolia.")
