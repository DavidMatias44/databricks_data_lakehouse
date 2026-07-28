from pathlib import Path
from shutil import copytree

project_path = Path.cwd().parent

data_dir = project_path / "data"
volume_dir = Path("/Volumes/data_lakehouse/raw/source_systems")

for directory in ["crm", "erp"]:
    copytree(data_dir / directory, volume_dir / directory, dirs_exist_ok=True)
