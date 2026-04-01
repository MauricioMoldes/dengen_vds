# DenGen VDS Pipeline

The **DenGen VDS pipeline** is a scalable workflow for generating **Variant Dataset (VDS)** files from gVCF inputs using Hail.

It is designed to process large cohorts (e.g., 24K+ genomes) efficiently on HPC systems by splitting the workload into **independent shards** and merging them into a final VDS.

This approach follows the same principles used by large-scale projects such as gnomAD, adapted for the **DenGen Danish population genomics project**.

## Project Structure
```
dengen_vds/
├── config/
│   └── config.yaml          # Central configuration (paths, sharding, reference)
├── src/
│   ├── shard/
│   │   └── dengen_shard.py  # Runs VDS combiner on a subset of samples
│   ├── merge/
│   │   └── dengen_merge.py  # Merges shard VDS files into final dataset
│   └── utils/
│       ├── io.py            # Path helpers (gVCFs, shards, tmp)
│       └── validation.py    # Input validation utilities
├── pbs/
│   ├── shards_individual/   # One PBS job per shard
│   └── dengen_merge.pbs     # Merge job
├── logs/
│   └── shards/              # Log files for each shard
├── results/
│   ├── shards/              # Intermediate VDS shards
│   └── final/               # Final merged VDS
├── tmp/                     # Temporary files for Hail/Spark
└── README.md
```


> **Note:** This repository does not include raw gVCFs, sample lists, or container images.

## Prerequisites

- Hail (>= 0.2.x)
- Python (>= 3.10)
- Singularity / Apptainer
- PBS / Moab HPC scheduler
- Access to HPC compute nodes
- Reference genome: GRCh38
- gVCF input files

### Optional

- Java (handled inside container)
- Spark (managed by Hail)

> The pipeline is designed to run inside a containerized environment using Singularity/Apptainer.

