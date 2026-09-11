import os
import shutil
import time
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 1. Define folder mappings by file extension
EXTENSION_MAP = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".csv", ".pptx"],
    "Archives": [".zip", ".tar", ".gz", ".7z", ".rar"],
    "Audio": [".mp3", ".wav", ".flac", ".aac"],
    "Video": [".mp4", ".mkv", ".mov", ".avi"],
    "Executables": [".exe", ".msi", ".dmg", ".pkg", ".deb"],
    "Code": [".py", ".js", ".html", ".css", ".json", ".sql"]
}

# 2. Setup logging configuration
logging.basicConfig(
    filename="organizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def get_unique_path(target_path: Path) -> Path:
    """Handles duplicate filenames by appending a numerical counter."""
    counter = 1
    new_path = target_path
    while new_path.exists():
        new_path = target_path.parent / f"{target_path.stem}_{counter}{target_path.suffix}"
        counter += 1
    return new_path

def organize_file(file_path: Path, watch_dir: Path):
    """Sorts a single file into its designated subfolder."""
    # Skip directories and the log file itself
    if file_path.is_dir() or file_path.name == "organizer.log":
        return

    extension = file_path.suffix.lower()
    dest_category = "Others"

    # Match extension to category
    for category, extensions in EXTENSION_MAP.items():
        if extension in extensions:
            dest_category = category
            break

    # Target directory setup
    category_dir = watch_dir / dest_category
    category_dir.mkdir(exist_ok=True)

    target_path = get_unique_path(category_dir / file_path.name)

    try:
        shutil.move(str(file_path), str(target_path))
        log_msg = f"Moved: {file_path.name} -> {dest_category}/"
        print(log_msg)
        logging.info(log_msg)
    except Exception as e:
        err_msg = f"Failed to move {file_path.name}: {e}"
        print(err_msg)
        logging.error(err_msg)


class FileHandler(FileSystemEventHandler):
    def __init__(self, watch_dir: Path):
        self.watch_dir = watch_dir

    def on_created(self, event):
        if not event.is_directory:
            # Short sleep to ensure browser/system finishes downloading/writing the file
            time.sleep(1)
            organize_file(Path(event.src_path), self.watch_dir)


def organize_existing_files(watch_dir: Path):
    """Organize any files currently sitting in the watch directory upon start."""
    print("Organizing existing files in directory...")
    for item in watch_dir.iterdir():
        if item.is_file():
            organize_file(item, watch_dir)


def main():
    # Change this path to your Downloads folder or any test folder
    WATCH_DIRECTORY = Path.home() / "Downloads"

    if not WATCH_DIRECTORY.exists():
        print(f"Error: Directory {WATCH_DIRECTORY} does not exist.")
        return

    # Process files already present
    organize_existing_files(WATCH_DIRECTORY)

    # Start watching for new files
    event_handler = FileHandler(WATCH_DIRECTORY)
    observer = Observer()
    observer.schedule(event_handler, str(WATCH_DIRECTORY), recursive=False)
    
    observer.start()
    print(f"\n[Active] Monitoring: {WATCH_DIRECTORY}")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopping directory monitor...")
    
    observer.join()


if __name__ == "__main__":
    main()