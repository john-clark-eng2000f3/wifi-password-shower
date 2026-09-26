# wifi-password-shower

I got tired of clicking through five layers of Windows adapter settings just to find a Wi-Fi password for a guest. This is a quick CLI tool to list, search, and show saved Wi-Fi profiles and their passwords directly from the terminal.

It wraps the Windows `netsh` utility, handles different console encodings, and parses the localized output (handles English, German, French, Spanish, and Russian Windows installations out of the box).

## Installation

Since this targets Windows, you can just clone it and install the single dependency for colored output:

```cmd
pip install -r requirements.txt
```

## Usage

Show all saved Wi-Fi networks and their passwords:

```cmd
python wifishow.py
```

Search for a specific network (case-insensitive fuzzy match):

```cmd
python wifishow.py Home
```

Show password only for a specific network (handy for scripting or copying to clipboard):

```cmd
python wifishow.py MyHomeWiFi --raw
```

Force a specific encoding if your Windows console is using something non-standard:

```cmd
python wifishow.py --encoding cp1251
```

<!-- verified: 2026-09-26 -->
