import argparse
import sys
import csv
import json
from wifishow.netsh import get_all_profiles, NetshError

def print_table(profiles):
    if not profiles:
        print("No saved Wi-Fi profiles found.")
        return

    # Calculate clean dynamic padding
    max_ssid = max(len(p.get("ssid", "")) for p in profiles)
    max_ssid = max(max_ssid, 4)
    max_auth = max(len(p.get("auth", "")) for p in profiles)
    max_auth = max(max_auth, 8)

    # print(f"DEBUG: padding widths: ssid={max_ssid}, auth={max_auth}")

    header = f"{'SSID':<{max_ssid}} | {'Security':<{max_auth}} | {'Password'}"
    print(header)
    print("-" * len(header))
    for p in profiles:
        ssid = p.get("ssid", "")
        auth = p.get("auth", "")
        password = p.get("password", "") or ""
        print(f"{ssid:<{max_ssid}} | {auth:<{max_auth}} | {password}")

def main():
    parser = argparse.ArgumentParser(
        description="Display saved Windows Wi-Fi profiles and passwords."
    )
    parser.add_argument("-s", "--search", help="Filter profiles by SSID (case-insensitive)")
    parser.add_argument("--no-passwords", action="store_true", help="Skip querying security payloads")
    parser.add_argument("--json", action="store_true", help="Output raw profiles list in JSON")
    parser.add_argument("--csv", action="store_true", help="Output raw profiles list in CSV")
    
    args = parser.parse_args()
    
    try:
        profiles = get_all_profiles(include_passwords=not args.no_passwords)
    except NetshError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
        
    if args.search:
        query = args.search.lower()
        profiles = [p for p in profiles if query in p.get("ssid", "").lower()]

    if args.json:
        print(json.dumps(profiles, indent=2, ensure_ascii=False))
        return

    if args.csv:
        writer = csv.writer(sys.stdout, lineterminator="\n")
        writer.writerow(["SSID", "Security", "Password"])
        for p in profiles:
            writer.writerow([p.get("ssid", ""), p.get("auth", ""), p.get("password", "")])
        return

    print_table(profiles)

if __name__ == "__main__":
    main()
