import sys
sys.path.append("/src")

import hail as hl
import glob
import re
import shutil

from config import cfg
from utils.io import get_tmp_path

# ----------------------------
# Config
# ----------------------------
EXPECTED_SHARDS = 116  # shards 0–115 only

# ----------------------------
# Initialize Hail
# ----------------------------
hl.init(default_reference=cfg["reference"])

# ----------------------------
# Helper: numeric shard sorting
# ----------------------------
def shard_key(path):
    match = re.search(r"shard_(\d+)\.vds", path)
    if not match:
        raise ValueError(f"Invalid shard filename: {path}")
    return int(match.group(1))

# ----------------------------
# Locate shard VDS files
# ----------------------------
vds_glob = f"{cfg['paths']['results']}/shards/*.vds"
vds_paths = glob.glob(vds_glob)

print(f"Found {len(vds_paths)} shard files (unsorted)")

# Safety: ensure we found something
if not vds_paths:
    raise RuntimeError("No VDS shards found. Check shard jobs.")

# Sort numerically
vds_paths = sorted(vds_paths, key=shard_key)

print(f"First 5 shards: {vds_paths[:5]}")
print(f"Last 5 shards: {vds_paths[-5:]}")

# ----------------------------
# Validate shard completeness
# ----------------------------
shard_ids = [shard_key(p) for p in vds_paths]

missing = sorted(set(range(EXPECTED_SHARDS)) - set(shard_ids))
extra = sorted(set(shard_ids) - set(range(EXPECTED_SHARDS)))

if missing:
    raise RuntimeError(f"Missing shards: {missing}")

if extra:
    print(f"Ignoring extra shards: {extra}")
    vds_paths = [p for p in vds_paths if shard_key(p) < EXPECTED_SHARDS]

if len(vds_paths) != EXPECTED_SHARDS:
    raise RuntimeError(
        f"Expected {EXPECTED_SHARDS} shards, found {len(vds_paths)}"
    )

print(f" Using {len(vds_paths)} shards for merge")

# ----------------------------
# Define output + tmp
# ----------------------------
output_path = f"{cfg['paths']['results']}/final/dengen.vds"
tmp_path = get_tmp_path("merge")

print(f"Merging into: {output_path}")
print(f"Using tmp: {tmp_path}")

# ----------------------------
# Clean tmp directory
# ----------------------------
print("Cleaning temporary directory...")
#shutil.rmtree(tmp_path, ignore_errors=True)

# ----------------------------
# Run combiner
# ----------------------------
combiner = hl.vds.new_combiner(
    output_path=output_path,
    temp_path=tmp_path,
    vds_paths=vds_paths
)

print("Starting merge...")
combiner.run()

print("Merge completed successfully")
