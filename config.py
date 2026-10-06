import ipaddress
import tomllib
from pathlib import Path
from typing import Any

CONFIG = Path("/data/adb/easytier/config.toml")


def load_config(path: Path = CONFIG) -> tuple[ipaddress.IPv4Network, dict[str, Any]]:
    with path.open("rb") as source:
        config = tomllib.load(source)
    address = ipaddress.IPv4Interface(config["ipv4"])
    # Android policy routing needs the same explicit subnet as the EasyTier TUN.
    if (
        config.get("dhcp", False)
        or "/" not in config["ipv4"]
        or address.network.prefixlen == 32
    ):
        raise ValueError(
            "Set a fixed ipv4 address with an explicit subnet prefix below /32"
        )
    return address.network, config["magisk"]["easytier"]
