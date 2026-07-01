import kagglehub
import shutil
from pathlib import Path

cache_path = Path(kagglehub.dataset_download(
    "beatafaron/hr-corporate-data-bilingual-enpl-bronze-layer"
))

target_dir = Path("data/company_bronze")

if not target_dir.exists():
    shutil.copytree(cache_path, target_dir)
    print(f"Copied dataset to {target_dir}")
else:
    print(f"{target_dir} already exists")