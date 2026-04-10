#!/bin/sh

SHARD_DIR="/ngc/projects2/gm/people/mauqua/hail-singularity/results/shards"

for shard in "$SHARD_DIR"/dengen_shard_*.vds; do

    [ -d "$shard" ] || continue

    ref="$shard/reference_data/_SUCCESS"
    var="$shard/variant_data/_SUCCESS"

    if [ ! -f "$ref" ] || [ ! -f "$var" ]; then
        basename "$shard" | sed 's/dengen_shard_\(.*\)\.vds/\1/'
    fi

done
