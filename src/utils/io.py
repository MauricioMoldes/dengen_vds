import os
from src.config import cfg

def get_gvcf_path(sample_id):
    return f"{cfg['paths']['base']}/{sample_id}_snv_germline_raw.haplotype_caller.g.vcf.gz"

def get_shard_output(shard_id):
    return f"{cfg['paths']['results']}/shards/dengen_shard_{shard_id}.vds"

def get_tmp_path(name):
    return f"{cfg['paths']['tmp']}/{name}"
