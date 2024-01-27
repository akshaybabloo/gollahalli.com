#!/bin/bash

webp_version="1.3.2"

if [ -n "$CI" ] || ! command -v cwebp &>/dev/null; then
    echo "Installing cwebp and gif2webp (forced installation in CI environment)."

    user_bin="$HOME/bin"
    mkdir -p "$user_bin"
    curl -L https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-${webp_version}-linux-x86-64.tar.gz -o /tmp/libwebp.tar.gz
    tar -xzf /tmp/libwebp.tar.gz -C /tmp
    mv /tmp/libwebp-${webp_version}-linux-x86-64/bin/* "$user_bin"

    chmod +x "$user_bin"/*

    rm -rf /tmp/libwebp-${webp_version}-linux-x86-64 /tmp/libwebp.tar.gz

    if ! grep -q "$user_bin" "$HOME/.bashrc"; then
        echo "export PATH=\"$user_bin:\$PATH\"" >>"$HOME/.bashrc"
        source "$HOME/.bashrc"
    fi

    echo -e "cwebp has been installed to $user_bin\n"
    cwebp_path="$user_bin/cwebp"
    gif2webp_path="$user_bin/gif2webp"
else
    echo -e "cwebp is already installed.\n"
    cwebp_path="cwebp"
    gif2webp_path="gif2webp"
fi

echo -e "cwebp version: $($cwebp_path -version)\n"
echo -e "gif2webp version: $($gif2webp_path -version)\n"

# Install poetry
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"

# Install dependencies
"$HOME/.local/bin/poetry" install
"$HOME/.local/bin/poetry" run python scripts/convert-webp.py
