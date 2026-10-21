import os
import shutil
from pathlib import Path

# Mapping file extensions to corresponding folder names
DIRECTORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"],
    "Archives": [".zip", ".tar", ".gz", ".rar", ".7z"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Video": [".mp4", ".mkv", ".mov", ".avi"],
    "Code_Scripts": [".py", ".sh", ".c", ".cpp", ".cs", ".php", ".sql", ".html", ".css", ".js"],
    "Executables_Installers": [".exe", ".msi", ".deb", ".apk", ".iso"],
}

def get_unique_path(target_path: Path) -> Path:
    """Handles name collisions by appending an incrementing index."""
    if not target_path.exists():
        return target_path
    
    stem = target_path.stem
    suffix = target_path.suffix
    parent = target_path.parent
    counter = 1
    
    while True:
        new_path = parent / f"{stem}_{counter}{suffix}"
        if not new_path.exists():
            return new_path
        counter += 1

def organize_folder(target_dir: str):
    base_path = Path(target_dir).resolve()

    if not base_path.exists() or not base_path.is_dir():
        print(f"Error: Invalid directory: {target_dir}")
        return

    # Avoid processing files that are already sorted into category folders
    category_folders = set(DIRECTORIES.keys()) | {"Others"}

    for item in base_path.iterdir():
        # Skip subdirectories and this script if run in the target directory
        if item.is_dir() or item.name == Path(__file__).name:
            continue

        file_ext = item.suffix.lower()
        destination_folder_name = "Others"

        for category, extensions in DIRECTORIES.items():
            if file_ext in extensions:
                destination_folder_name = category
                break

        dest_dir = base_path / destination_folder_name
        dest_dir.mkdir(exist_ok=True)

        target_file_path = get_unique_path(dest_dir / item.name)
        
        try:
            shutil.move(str(item), str(target_file_path))
            print(f"Moved: {item.name} -> {destination_folder_name}/")
        except Exception as e:
            print(f"Failed to move {item.name}: {e}")

if __name__ == "__main__":
    # Point this to Downloads, Desktop, or test folder
    folder_to_clean = os.path.expanduser("~/Downloads")
    print(f"Organizing: {folder_to_clean}")
    organize_folder(folder_to_clean)