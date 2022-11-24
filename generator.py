# The rootfs generator, this script can only be run on a debian environment
# as it uses `mmdebstrap`, which is only available on debian distros

import shutil
import sys

# check if mmdebstrap exists
if shutil.which("mmdebstrap") is None:
    print("mmdebstrap does not exists", file=sys.stderr)
    exit(1)

import subprocess
import toml

# load the config file
config = None
with open("config.toml", "r") as f:
    config = toml.load(f)

# generate the sources-list and write it to a file
sources = "\n".join(config["build"]["sources-list"])
with open("mmdebstrap-sources.list", "w") as f:
    f.write(sources)
    f.flush()

mmdebstrap_process = subprocess.Popen(
    [
     "mmdebstrap",
     "--architectures", config["build"]["arch"],
     "--verbose",
     "--include=" + ",".join(config["build"]["packages"]),
     "",
     config["build"]["outdir"],
    ],
    stdin=subprocess.PIPE,
    shell=True
)

mmdebstrap_process.communicate(input=sources.encode())
mmdebstrap_process.wait()
