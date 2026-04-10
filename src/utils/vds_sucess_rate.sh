#!/bin/sh

SHARD_DIR="/ngc/projects2/gm/people/mauqua/hail-singularity/results/shards"

total=0
success=0

for shard in "$SHARD_DIR"/dengen_shard_*.vds; do

    # Skip if no match (POSIX safety)
    [ -d "$shard" ] || continue

    total=$((total + 1))

    ref_success="$shard/reference_data/_SUCCESS"
    var_success="$shard/variant_data/_SUCCESS"

    if [ -f "$ref_success" ] && [ -f "$var_success" ]; then
        success=$((success + 1))
    fi

done

# Avoid division by zero
if [ "$total" -eq 0 ]; then
    echo "No shards found."
    exit 0
fi

# Compute percentage (POSIX safe)
percent=$(awk "BEGIN {printf \"%.2f\", ($success/$total)*100}")

echo "=============================="
echo "DenGen VDS Shard Status"
echo "=============================="
echo "Total shards     : $total"
echo "Successful shards: $success"
echo "Failed/partial   : $((total - success))"
echo "Success rate     : $percent %"
echo "=============================="
