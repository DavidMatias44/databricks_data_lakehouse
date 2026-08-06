import logging
from pathlib import Path
from shutil import copytree, Error

from utils.config import raw_data_path, raw_volume_path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("preparation")


def copy_files_into_volume(src_path: Path = raw_data_path, dst_path: Path = raw_volume_path) -> None:
    """Copy files from the `src_path` into the `dst_path`"""

    if not src_path.exists():
        raise FileNotFoundError(f"Source path does not exist: {src_path}") 
    
    try:
        for item in src_path.iterdir():
            if not item.is_dir():
                continue
            
            system_name = item.name
            logger.info(f"Copying from: {src_path / system_name} to: {dst_path / system_name}")
            copytree(src_path / system_name, dst_path / system_name, dirs_exist_ok=True)
            logger.info(f"Success!")
    except Error as e:
        logger.exception(f"Unable to copy files due to: {e}")


if __name__ == "__main__":
    copy_files_into_volume()
