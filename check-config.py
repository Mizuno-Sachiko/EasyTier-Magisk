import ipaddress
from pathlib import Path

from config import load_config

network, settings = load_config(Path(__file__).with_name("config.example.toml"))
assert network == ipaddress.IPv4Network("192.0.2.0/24")
assert settings["state_dir"] == "/data/adb/easytier"
assert settings["route_priority"] < settings["root_rule_priority"]
assert settings["root_rule_priority"] < settings["root_rule_target"]
print("TOML network and module settings checks passed")
