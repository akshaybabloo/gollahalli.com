#!/bin/bash -x

webp_version="1.3.1"

if ! command -v cwebp &>/dev/null; then
    user_bin="$HOME/bin"

    mkdir -p "$user_bin"
    wget https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-${webp_version}-linux-x86-64.tar.gz -O /tmp/libwebp.tar.gz
    tar -xzf /tmp/libwebp.tar.gz -C /tmp
    mv /tmp/libwebp-${webp_version}-linux-x86-64/bin/cwebp "$user_bin"

    chmod +x "$user_bin/cwebp"

    rm -rf /tmp/libwebp-${webp_version}-linux-x86-64 /tmp/libwebp.tar.gz

    if ! grep -q "$user_bin" "$HOME/.bashrc"; then
        echo "export PATH=\"$user_bin:\$PATH\"" >>"$HOME/.bashrc"
        source "$HOME/.bashrc"
    fi

    echo "cwebp has been installed to $user_bin"
else
    echo "cwebp is already installed."
fi

cwebp_path="$user_bin/cwebp"
scriptLocation="$(dirname "$(readlink -f "$0")")"
parentDirectory="$(dirname "$scriptLocation")"

imageExtensions=("*.jpg" "*.png")
echo "Converting images to .webp format in $parentDirectory"

for extension in "${imageExtensions[@]}"; do
    find "$parentDirectory" -type f -name "$extension" | while read -r imageFile; do
        newFileName="${imageFile%.*}.webp"

        originalSizeBytes=$(stat -c%s "$imageFile")
        originalSize=""

        if [[ originalSizeBytes -ge 1048576 ]]; then
            originalSize=$(awk -v bytes="$originalSizeBytes" 'BEGIN {printf "%.2f MB", bytes/1048576}')
        else
            originalSize=$(awk -v bytes="$originalSizeBytes" 'BEGIN {printf "%.2f KB", bytes/1024}')
        fi

        # Convert the image to .webp format with quality 75 and capture the error message if any
        conversionError=$("$cwebp_path" -mt -q 75 "$imageFile" -o "$newFileName" 2>&1)

        # Check if the command succeeded
        if [[ $? -eq 0 ]]; then
            newSizeBytes=$(stat -c%s "$newFileName")
            newSize=""

            if [[ newSizeBytes -ge 1048576 ]]; then
                newSize=$(awk -v bytes="$newSizeBytes" 'BEGIN {printf "%.2f MB", bytes/1048576}')
            else
                newSize=$(awk -v bytes="$newSizeBytes" 'BEGIN {printf "%.2f KB", bytes/1024}')
            fi

            echo "Converted $(basename "$imageFile") ($originalSize) to $(basename "$newFileName") ($newSize) - ✅"
        else
            echo "Failed to convert $(basename "$imageFile") ($originalSize) to $(basename "$newFileName") - ❌"
            echo "Error: $conversionError"
        fi
    done
done
