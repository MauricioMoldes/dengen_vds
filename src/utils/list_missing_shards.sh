#!/bin/sh

SHARD_DIR="/ngc/projects2/gm/people/mauqua/hail-singularity/results/shards"
TOTAL_SHARDS=120

i=0
while [ "$i" -lt "$TOTAL_SHARDS" ]; do

    shard_path="${SHARD_DIR}/dengen_shard_${i}.vds"

    if [ ! -d "$shard_path" ]; then
        echo "$i"
    fi

    i=$((i + 1))
done
