import asyncio
import os
from pathlib import Path

import aiofiles.os as aos
import humanize
from rich.console import Console

console = Console()
if os.environ.get("CI"):
    console = Console(force_terminal=False)


async def get_file_size(file_path: Path) -> str:
    """
    Returns the size of a file in KB or MB

    :param file_path: File path
    :return: File size in KB or MB
    """
    size_bytes = await aos.path.getsize(file_path)
    return humanize.naturalsize(size_bytes, binary=True)


async def convert_image(image_path: Path, cwebp_path: str, gif2webp_path: str) -> None:
    """
    Converts an image to webp format

    :param image_path: Path to the image file
    :param cwebp_path: Path to the cwebp executable
    :param gif2webp_path: Path to the gif2webp executable
    """
    new_file_name = image_path.with_suffix(".webp")

    # Skip if the webp version of the file already exists
    if new_file_name.exists():
        print(f"Skipped conversion for {image_path.name}: .webp file already exists.")
        return

    original_size = await get_file_size(image_path)
    if image_path.suffix.lower() == ".gif":
        conversion_command = [
            gif2webp_path,
            "-mt",
            "-lossy",
            "-q",
            "75",
            str(image_path),
            "-o",
            str(new_file_name),
            "-quiet",
        ]
    else:
        conversion_command = [
            cwebp_path,
            "-mt",
            "-q",
            "75",
            str(image_path),
            "-o",
            str(new_file_name),
            "-quiet",
        ]

    try:
        process = await asyncio.create_subprocess_exec(*conversion_command)
        await process.wait()
        new_size = await get_file_size(new_file_name)
        console.print(
            f"Converted {image_path.name} ({original_size}) to {new_file_name.name} ({new_size}) - :white_check_mark:",
            style="bold green",
        )
    except Exception as e:
        console.print(
            f"Failed to convert {image_path.name} ({original_size}) to {new_file_name.name} - :cross_mark:",
            style="bold red",
        )
        print(f"Error: {e}")


async def main():
    script_location = Path(__file__).parent
    parent_directory = script_location.parent

    image_extensions = ["*.jpg", "*.png", "*.gif"]
    console.print(f"Converting images to .webp format in {parent_directory}", style="bold blue", end="\n\n")

    image_files = [p for ext in image_extensions for p in parent_directory.glob(f"**/{ext}")]

    cwebp_path = "cwebp"  # Update with the actual path if necessary
    gif2webp_path = "gif2webp"  # Update with the actual path if necessary

    tasks = [convert_image(image_file, cwebp_path, gif2webp_path) for image_file in image_files]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
