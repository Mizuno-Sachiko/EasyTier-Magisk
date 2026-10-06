import argparse
import hashlib
import json
import zipfile
from pathlib import Path

parser = argparse.ArgumentParser(
    description="Build a credential-free EasyTier Magisk module"
)
parser.add_argument("--source", type=Path, required=True, help="Official Magisk ZIP")
parser.add_argument("--sha256", required=True, help="Verified official ZIP SHA-256")
parser.add_argument("--version", required=True)
parser.add_argument("--version-code", type=int, required=True)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
if hashlib.sha256(args.source.read_bytes()).hexdigest() != args.sha256:
    raise ValueError("Official source SHA-256 mismatch")
root = Path(__file__).resolve().parent
repository = "https://github.com/Mizuno-Sachiko/EasyTier-Magisk"
core_version = args.version.rsplit("-", 1)[0]
args.output.parent.mkdir(parents=True, exist_ok=True)
# Exclusive creation preserves existing release artifacts.
with (
    zipfile.ZipFile(args.source) as source,
    zipfile.ZipFile(args.output, "x", zipfile.ZIP_DEFLATED) as output,
):
    for name in [
        "META-INF/com/google/android/update-binary",
        "META-INF/com/google/android/updater-script",
        "easytier-core",
        "easytier-cli",
    ]:
        output.writestr(name, source.read(name))
    for name in [
        "service.sh",
        "run.py",
        "config.py",
        "customize.sh",
        "README.md",
        "LICENSE",
        "licenses/EasyTier.LICENSE",
    ]:
        output.writestr(name, (root / name).read_bytes())
    output.writestr(
        "module.prop",
        f"""id=easytier_personal
name=EasyTier for Magisk
version={args.version}
versionCode={args.version_code}
author=contributors
description=Root EasyTier with private TOML configuration and Android VPN coexistence. Requires Termux Python. No persistent wake lock.
updateJson={repository}/releases/latest/download/update.json
coreSource=https://github.com/EasyTier/EasyTier/tree/v{core_version}
""",
    )
    # Runtime writes the configured resolvers into the file Magisk maps at boot.
    output.writestr(
        "system/etc/resolv.conf",
        "# Resolvers are supplied by the private module configuration.\n",
    )
# The latest Release supplies the manifest; downloads stay tied to its version.
release = f"{repository}/releases/download/v{args.version}"
with args.output.with_name("update.json").open("x", encoding="utf-8") as output:
    json.dump(
        {
            "version": args.version,
            "versionCode": args.version_code,
            "zipUrl": f"{release}/{args.output.name}",
            "changelog": f"{release}/changelog.md",
        },
        output,
        indent=2,
    )
    output.write("\n")
print(args.output)
