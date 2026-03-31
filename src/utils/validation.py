import os

def validate_gvcfs(paths):
    missing = [p for p in paths if not os.path.exists(p)]
    
    if missing:
        raise FileNotFoundError(f"Missing {len(missing)} gVCFs")
