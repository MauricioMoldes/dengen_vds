#!/bin/sh

DELAY=3600   # seconds (7200 = 2h, 3600 = 1h)

LIST_SCRIPT="/ngc/projects2/gm/people/mauqua/hail-singularity/src/utils/list_missing_shards.sh"
PBS_DIR="/ngc/projects2/gm/people/mauqua/hail-singularity/pbs"

echo "Starting slow submission (delay = $DELAY sec)"

bash "$LIST_SCRIPT" | while read i; do

    # Skip if already running (extra safety)
    if qstat -u mauqua | grep -q "dengen_shard_${i}"; then
        echo "Skipping shard $i (already running)"
        continue
    fi

    qsub "${PBS_DIR}/shard_${i}.pbs"
    echo "Submitted shard $i at $(date)"

    sleep "$DELAY"

done

echo "All missing shards submitted."
