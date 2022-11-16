# The rootfs generator, this script can only be run on a debian environment
# as it uses `mmdebstrap`, which is only available on debian distros

import subprocess
import tomllib

# load the config file
config = None
with open("config.toml", "rb") as f:
    config = tomllib.load(f)

with open("sources_list.txt", "rw") as f:
    f.write("\n".join(config["mmdebstrap"]["sources-list"]))

subprocess.check_call(
    ["mmdebstrap",
     "--architectures", config["mmdebstrap"]["arch"],
     "--verbose",
     "--include=", "m".join(config["mmdebstrap"]["packages"]),
     config["mmdebstrap"]["outdir"],
     "sources_list.txt"
     ]
)
