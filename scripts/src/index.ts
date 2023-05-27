import algoliasearch from "algoliasearch";
import path from "path";
import fs from "fs";
import toml from "toml";
import * as process from "process";

console.log("-------------------------------------------");
console.log("Deploying search index");

const APP_ID = "UT1XVMZE1Q";
const INDEX_NAME = "gollahalli-website";
const FILE_PATH = path.join('..', 'public', 'searchindex.json');
const CLIENT_SECRET = process.env.ALGOLIA_KEY;
if (!CLIENT_SECRET) {
    throw new Error('Algolia key not found');
}

/* Update the search index */
const client = algoliasearch(APP_ID, CLIENT_SECRET!);
const index = client.initIndex(INDEX_NAME);
try {
    fs.existsSync(FILE_PATH);
} catch (e) {
    console.error(e);
    process.exit(1);
}
const data = JSON.parse(fs.readFileSync(FILE_PATH, 'utf8'));
console.log("Clearing previous search entries");
index.clearObjects();
console.log("Adding new search entries");
index.saveObjects(data, {autoGenerateObjectIDIfNotExist: true});

/* Trigger a reindex */
const config = toml.parse(fs.readFileSync(path.join('..', 'config.toml'), 'utf8'));
console.log(`Content deployed at ${config.baseURL}`);


