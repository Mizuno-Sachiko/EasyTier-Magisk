import fcntl
import ipaddress
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

from config import CONFIG, load_config

MODULE = Path(__file__).resolve().parent
IP = "/system/bin/ip"
os.umask(0o077)
network, settings = load_config()
state = Path(settings["state_dir"])
core_command = [
    str(MODULE / "easytier-core"),
    "-c",
    str(CONFIG),
    "--rpc-portal",
    settings["rpc_portal"],
    "--console-log-level",
    "off",
    "--file-log-level",
    "warn",
    "--file-log-dir",
    str(state),
    "--file-log-size",
    str(settings["log_size_mb"]),
    "--file-log-count",
    str(settings["log_count"]),
]
resolver_text = "".join(
    f"nameserver {ipaddress.ip_address(address)}\n"
    for address in settings["dns_servers"]
)
rules = [
    (
        "-4",
        [
            "priority",
            str(settings["route_priority"]),
            "to",
            str(network),
            "lookup",
            "main",
        ],
    ),
    *[
        (
            family,
            [
                "priority",
                str(settings["root_rule_priority"]),
                "iif",
                "lo",
                "uidrange",
                "0-0",
                "goto",
                str(settings["root_rule_target"]),
            ],
        )
        for family in ("-4", "-6")
    ],
]
if sys.argv[1:] == ["--check-config"]:
    subprocess.run(
        [str(MODULE / "easytier-core"), "-c", str(CONFIG), "--check-config"],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    sys.exit(0)
if (MODULE / "disable").exists():
    sys.exit(0)

state.mkdir(mode=0o700, parents=True, exist_ok=True)
lock = (state / "service.lock").open("a")
fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
# Keep the inode Magisk mapped at boot; the mounted resolver sees these contents.
(MODULE / "system/etc/resolv.conf").write_text(resolver_text)
installed: list[tuple[str, list[str]]] = []
child: subprocess.Popen[bytes] | None = None
stopping = False


def stop(_signum: int, _frame: object) -> None:
    global stopping
    stopping = True
    if child is not None and child.poll() is None:
        child.terminate()


signal.signal(signal.SIGTERM, stop)
signal.signal(signal.SIGINT, stop)
try:
    for family, fields in rules:
        subprocess.run([IP, family, "rule", "add", *fields], check=True)
        installed.append((family, fields))
    with (state / "service.log").open("a") as log:
        # Wait for process exits; no idle polling or wake lock is needed.
        while not stopping and not (MODULE / "disable").exists():
            child = subprocess.Popen(core_command, stdout=log, stderr=subprocess.STDOUT)
            if stopping:
                child.terminate()
            status = child.wait()
            child = None
            if status == 0 or stopping:
                break
            time.sleep(5)
finally:
    if child is not None and child.poll() is None:
        child.terminate()
        child.wait()
    for family, fields in reversed(installed):
        subprocess.run([IP, family, "rule", "del", *fields], check=True)
    lock.close()
