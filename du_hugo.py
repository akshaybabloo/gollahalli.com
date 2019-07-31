import os
import platform
import tarfile
import tempfile
from pathlib import Path

import requests
import yaml

with open('azure-pipeline.yml') as f:
    try:
        hugo_version = yaml.safe_load(f)['variables']['HUGO_VERSION']
    except yaml.YAMLError as exc:
        print(exc)

location = os.path.join(str(Path.home()), 'bin')
os_type = platform.system()

download_url_mac = f"https://github.com/gohugoio/hugo/releases/download/v{hugo_version}/hugo_extended_{hugo_version}_macOS-64bit.tar.gz"
download_url_windows = f"https://github.com/gohugoio/hugo/releases/download/v{hugo_version}/hugo_{hugo_version}_Windows-64bit.zip"

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
    with tarfile.open(filepath, "r:gz") as f:
        f.extract("hugo", location)


if __name__ == '__main__':
    download()
    extract_file_and_move()
