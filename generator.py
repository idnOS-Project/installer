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
     "--architectures=" + config["build"]["arch"],
     "--verbose",
     "--format=tar",
     "--include=" + ",".join(config["build"]["packages"]),
    ],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    shell=True
)

tar_output = mmdebstrap_process.communicate(input=sources.encode())[0]
mmdebstrap_process.wait()

with open("output.tar", "wb") as f:
    f.write(tar_output)
