#!/bin/sh

# =========================
# CONFIG
# =========================
SHARD_RESULTS="/ngc/projects2/gm/people/mauqua/hail-singularity/results/shards"
#PBS_DIR="/ngc/projects2/gm/people/mauqua/hail-singularity/pbs/shards_individual"
PBS_DIR="/ngc/projects2/gm/people/mauqua/hail-singularity/pbs"

TOTAL_SHARDS=120
BATCH_SIZE=30

# =========================
# TEMP FILE
# =========================
TMP_FILE=$(mktemp)

echo "Scanning for missing shards..."

# =========================
# FIND MISSING SHARDS
# =========================
i=0
while [ "$i" -lt "$TOTAL_SHARDS" ]; do
    shard_dir="${SHARD_RESULTS}/dengen_shard_${i}.vds"
    pbs_file="${PBS_DIR}/shard_${i}.pbs"

    if [ ! -d "$shard_dir" ]; then
        if [ -f "$pbs_file" ]; then
            echo "$pbs_file" >> "$TMP_FILE"
        else
            echo "Warning: PBS file missing for shard $i"
        fi
    fi

    i=$((i + 1))
done

# =========================
# COUNT + EARLY EXIT
# =========================
TOTAL_MISSING=$(wc -l < "$TMP_FILE")

if [ "$TOTAL_MISSING" -eq 0 ]; then
    echo "All shards already exist. Nothing to submit."
    rm "$TMP_FILE"
    exit 0
fi

echo "Found $TOTAL_MISSING missing shards"

# =========================
# RANDOM SUBMISSION
# =========================
echo "Submitting up to $BATCH_SIZE shards..."

shuf "$TMP_FILE" | head -n "$BATCH_SIZE" | while read -r pbs_file; do
    qsub "$pbs_file"
    echo "Submitted $pbs_file"
done

# =========================
# CLEANUP
# =========================
rm "$TMP_FILE"

echo "Done."
