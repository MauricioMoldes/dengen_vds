import sys
sys.path.append("/src")

import hail as hl
import math

from config import cfg
from utils.io import get_gvcf_path, get_shard_output, get_tmp_path
from utils.validation import validate_gvcfs

hl.init(default_reference=cfg["reference"])

if len(sys.argv) < 2:
    raise ValueError("Shard ID argument missing")

shard_id = int(sys.argv[1])

# LOAD SAMPLES
with open(cfg["paths"]["samples"]) as f:
    samples = [line.strip() for line in f if line.strip()]

print(f"Total samples: {len(samples)}")

# SHARDING
shard_size = cfg["sharding"]["shard_size"]

start = shard_id * shard_size
end = start + shard_size

print(f"Shard {shard_id}: range {start}-{end}")

chunk = samples[start:end]

if not chunk:
    print(f"Shard {shard_id} empty")
    exit(0)

# BUILD PATHS
gvcfs = [get_gvcf_path(s) for s in chunk]

print(f"Shard {shard_id}: {len(gvcfs)} samples")

# VALIDATE
validate_gvcfs(gvcfs)

# OUTPUT
output_path = get_shard_output(shard_id)
tmp_path = get_tmp_path(f"shard_{shard_id}")

# COMBINER
combiner = hl.vds.new_combiner(
    output_path=output_path,
    temp_path=tmp_path,
    gvcf_paths=gvcfs,
    use_genome_default_intervals=True,
    gvcf_batch_size=cfg["sharding"]["gvcf_batch_size"]
)

combiner.run()
