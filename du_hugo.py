import os
import platform
import subprocess
import sys
import tarfile
import tempfile
import zipfile
from pathlib import Path

import requests
import yaml

try:
    with open('azure-pipeline.yml') as f:
        try:
            hugo_version = yaml.safe_load(f)['variables']['HUGO_VERSION']
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)
except FileNotFoundError:
    sys.exit(1)

location = os.path.join(str(Path.home()), 'bin')
os_type = platform.system()

download_url_mac = f"https://github.com/gohugoio/hugo/releases/download/v{hugo_version}/hugo_extended_{hugo_version}_macOS-64bit.tar.gz"
download_url_windows = f"https://github.com/gohugoio/hugo/releases/download/v{hugo_version}/hugo_extended_{hugo_version}_Windows-64bit.zip"

temp_folder = tempfile.gettempdir()
filepath = os.path.join(temp_folder, f"hugo_{hugo_version}")


def download():
    """
    Download the Hugo file to temp folder.
    """
    with open(filepath, "wb") as file:
        if os_type == 'Darwin':
            response = requests.get(download_url_mac, stream=True)
        elif os_type == 'Windows':
            response = requests.get(download_url_windows, stream=True)
        else:
            raise OSError("Not supported.")

        if response.headers.get('Status') == "404 Not Found":
            raise requests.exceptions.HTTPError("File not found")

        print("Downloading to: ", temp_folder)
        file.write(response.content)


def extract_file_and_move():
    """
    Extract the ``hugo`` file to the temp folder
    """
    print("Extracting and moving file to: ", location)
    if os_type == 'Darwin':
        with tarfile.open(filepath, "r:gz") as f:
            f.extract("hugo", location)
    elif os_type == 'Windows':
        with zipfile.ZipFile(filepath, "r") as f:
            f.extract("hugo.exe", location)


def confirm_update():
    """
    Checks if Hugo is updated or not.
    """

    print("Confirming upgrade")

    try:
        new_hugo_version = subprocess.check_output(["hugo", "version"]).strip()
        new_hugo_version = new_hugo_version.decode('utf-8').split(" ")[4].split("/")[0]
        print(".Net Version found: {}".format(new_hugo_version))
    except FileNotFoundError as e:
        raise

    if not 'v' + hugo_version == new_hugo_version:
        print("Hugo was not updated correctly")
        sys.exit(1)

    print("Updated.")

if __name__ == '__main__':
    download()
    extract_file_and_move()
    confirm_update()
