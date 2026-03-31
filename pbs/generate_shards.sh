#!/bin/sh
# POSIX-compliant shell

TEMPLATE="shard_template.pbs"
OUTPUT_DIR="./"

# Number of shards
NUM_SHARDS=120

i=0
while [ "$i" -lt "$NUM_SHARDS" ]; do
    OUTPUT_FILE="${OUTPUT_DIR}/shard_${i}.pbs"
    # Replace {{SHARD_INDEX}} in template
    sed "s/{{SHARD_INDEX}}/$i/g" "$TEMPLATE" > "$OUTPUT_FILE"
    i=$((i + 1))
done

echo "Generated $NUM_SHARDS shard PBS scripts in $OUTPUT_DIR"
