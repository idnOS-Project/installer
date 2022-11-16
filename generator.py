# The rootfs generator, this script can only be run on a debian environment
# as it uses `mmdebstrap`, which is only available on debian distros

import shutil
import sys

# check if mmdebstrap exists
if shutil.which("mmdebstrap") is None:
    print("mmdebstrap does not exists", file=sys.stderr)
    exit(1)

import subprocess
import tomllib

# load the config file
config = None
with open("config.toml", "rb") as f:
    config = tomllib.load(f)

output = subprocess.run(
    [
     "mmdebstrap",
     "--architectures", config["mmdebstrap"]["arch"],
     "--verbose",
     "--include=", "m".join(config["mmdebstrap"]["packages"]),
     config["mmdebstrap"]["outdir"],
    ],
    input="\n".join(config["mmdebstrap"]["sources-list"]),
    text=True
)
