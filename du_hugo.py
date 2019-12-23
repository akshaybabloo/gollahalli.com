import json
import os
import platform
import subprocess
import sys
import tarfile
import tempfile
import zipfile
from pathlib import Path

import requests
import toml
from tqdm import tqdm

try:
    with open('netlify.toml') as f:
        NETLIFY_CONFIG = toml.load(f)
        CURRENT_HUGO_VERSION = NETLIFY_CONFIG['context']['production']['environment']['HUGO_VERSION']
except Exception:
    raise

HUGO_BINARY_LOCATION = os.path.join(str(Path.home()), 'bin')
OS_TYPE = platform.system()
TEMP_FOLDER_PATH = tempfile.gettempdir()


def check_for_updates(override_version: str = None) -> str:
    """
    Checks for new Hugo version.

    :return: Version number or None
    """
    hugo_response = requests.get("https://api.github.com/repos/gohugoio/hugo/releases/latest")
    hugo_response = json.loads(hugo_response.content.decode('utf-8'))['tag_name'][1:]

    if override_version is not None:
        return override_version

    if not hugo_response == CURRENT_HUGO_VERSION:
        print(f"New update found. Current version {CURRENT_HUGO_VERSION}, new version {hugo_response}")

        answer = input("> Do you want to update to the newer version? (Y/n) ")

        if answer == '':
            print("Please select the correct option.")
            sys.exit(1)
        elif answer.lower() != 'y' and answer.lower() != 'n':
            print("Please select either 'y' or 'n'.")
            sys.exit(1)

        if answer.lower() == 'y':
            return hugo_response

        if answer.lower() == 'n':
            sys.exit(0)


def download(version: str, download_to: str):
    """
    Download the Hugo file to temp folder.

    :param version: Version number to download
    :param download_to: Path to download to
    """

    with open(download_to, "wb") as file:
        if OS_TYPE == 'Darwin':
            response = requests.get(
                f"https://github.com/gohugoio/hugo/releases/download/v{version}/hugo_extended_{version}_macOS-64bit.tar.gz",
                stream=True)
        elif OS_TYPE == 'Windows':
            response = requests.get(
                f"https://github.com/gohugoio/hugo/releases/download/v{version}/hugo_extended_{version}_Windows-64bit.zip",
                stream=True)
        else:
            raise OSError(f"{OS_TYPE} not supported.")

        if response.headers.get('Status') == "404 Not Found":
            raise requests.exceptions.HTTPError("File not found")

        print(f"Downloading Hugo v{version} to: ", download_to)
        total_length = int(response.headers.get('content-length'))

        if total_length is None:
            file.write(response.content)
        else:
            with tqdm(total=total_length / (32 * 1024.0), unit='B', unit_scale=True, unit_divisor=1024) as pbar:
                for data in response.iter_content(chunk_size=32 * 1024):
                    file.write(data)
                    pbar.update(len(data))


def extract_file_and_move(extract_from: str, move_to: str):
    """
    Extract the ``hugo`` file to the temp folder

    :param extract_from: ZIP or TAR absolute path
    :param move_to: Path to move uncompressed file
    """

    print("Extracting and moving file to: ", move_to)
    if OS_TYPE == 'Darwin':
        with tarfile.open(extract_from, "r:gz") as f:
            f.extract("hugo", move_to)
    elif OS_TYPE == 'Windows':
        with zipfile.ZipFile(extract_from, "r") as f:
            f.extract("hugo.exe", move_to)


def update_version_in_netlify(version: str):
    """
    Updates the Hugo version in ``netlify.toml`` file.

    :param version: Hugo version number
    """

    try:
        with open('netlify.toml', 'w') as pipeline:
            NETLIFY_CONFIG['context']['production']['environment']['HUGO_VERSION']=version
            NETLIFY_CONFIG['context']['deploy-preview']['environment']['HUGO_VERSION']=version

            toml.dump(NETLIFY_CONFIG, pipeline)

    except Exception:
        raise


def confirm_update():
    """
    Checks if Hugo is updated or not.
    """

    try:
        with open('netlify.toml') as f:
            update_hugo_version = toml.load(f)['context']['production']['environment']['HUGO_VERSION']
    except Exception:
        raise

    new_hugo_version = ''
    print("Confirming update")

    try:
        if OS_TYPE == 'Darwin':
            new_hugo_version = subprocess.check_output(["hugo", "version"]).strip()
            new_hugo_version = new_hugo_version.decode('utf-8').split(" ")[4].split("/")[0].split("-")[0]
        elif OS_TYPE == 'Windows':
            new_hugo_version = subprocess.check_output(["hugo", "version"]).strip()
            new_hugo_version = new_hugo_version.decode('utf-8').split(" ")[4].split("/")[0]
    except FileNotFoundError as e:
        raise

    if not 'v' + update_hugo_version == new_hugo_version:
        print("Hugo was not updated correctly")
        sys.exit(1)

    print("All done!")


# --------------------------------------------------------------


def main():
    new_version = check_for_updates()

    if new_version is None:
        print("No updates available")
        sys.exit(0)

    download_to_extract_from = os.path.join(TEMP_FOLDER_PATH, f"hugo_{new_version}")

    download(new_version, download_to_extract_from)
    extract_file_and_move(download_to_extract_from, HUGO_BINARY_LOCATION)
    update_version_in_netlify(new_version)
    confirm_update()


if __name__ == '__main__':
    main()
