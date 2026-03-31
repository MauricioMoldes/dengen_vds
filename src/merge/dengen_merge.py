import sys
sys.path.append("/src")

import hail as hl
import glob

from config import cfg
from utils.io import get_tmp_path

# Initialize Hail
hl.init(default_reference=cfg["reference"])

# Locate shard VDS files
vds_paths = sorted(glob.glob(f"{cfg['paths']['results']}/shards/*.vds"))

print(f"Found {len(vds_paths)} shards")

# 🚨 Safety check
if not vds_paths:
    raise RuntimeError("No VDS shards found. Check shard jobs.")

# Debug visibility
print(f"First 5 shards: {vds_paths[:5]}")

# Define output and temp paths
output_path = f"{cfg['paths']['results']}/final/dengen.vds"
tmp_path = get_tmp_path("merge")

print(f"Merging into: {output_path}")
print(f"Using tmp: {tmp_path}")

# Run combiner
combiner = hl.vds.new_combiner(
    output_path=output_path,
    temp_path=tmp_path,
    vds_paths=vds_paths
)

combiner.run()
