# Bluetooth-DDos

-
🔥 APT-Style Bluetooth Attack Toolkit

This Python script simulates advanced Bluetooth attacks inspired by real-world APT (Advanced Persistent Threat) tactics — such as MAC spoofing, OBEX file drop, ping floods, connect flooding, and vendor fingerprinting.

> ⚠️ **For educational and red-team simulation use ONLY. Do NOT use this on devices you don't own or without explicit permission.**

---

## 📦 Features

- 🔍 Bluetooth Device Discovery (10-sec scan)
- 🎯 Vendor Fingerprinting (Xiaomi, JBL, Raspberry Pi, etc.)
- 🎭 MAC Address Spoofing using `bdaddr`
- 📡 Bluetooth DDoS (l2ping + rfcomm connect flood)
- 💣 OBEX Push File Attack (via `obexftp`)
- 📂 Device Class & Name Spoofing (e.g., mimic JBL speaker)
- 🧠 Smart Targeting (mark known vulnerable vendors)

---

## 🧰 Requirements

Tested on **Kali Linux**, but works on most Debian-based systems with Bluetooth stack.

### Install dependencies:
```bash
sudo apt update
sudo apt install bluez obexftp bdaddr rfkill
pip3 install pybluez

Recommended Bluetooth Adapter:

Internal or external USB Bluetooth adapter

Must support raw L2CAP and OBEX (Class 1 preferred)



---

🚀 Usage

1. Make sure payload.txt (or any file you want to push) exists:



echo "Hello from attacker!" > payload.txt

2. Run the script:



sudo python3 bt_attack.py

3. Select a target from the list of discovered Bluetooth devices.



The script will:

Spoof your MAC, device name, and class

Scan nearby Bluetooth devices and mark vulnerable vendors

Let you pick a target

Attempt to push payload.txt via OBEX

Launch DDoS (l2ping + rfcomm connect flood)



---

🧪 What Each Module Does

Module	Description

spoof_identity	Changes your Bluetooth MAC address, name, and class
scan_devices	Scans for discoverable Bluetooth devices
match_vendor	Tags known vendors with vulnerabilities
obex_push	Pushes a file via OBEX (like APKs or payloads)
l2ping_flood	Sends repeated Bluetooth pings (Denial of Service)
connect_flood	Tries to connect repeatedly via RFCOMM
ddos	Launches multi-threaded Bluetooth attack



---

🔐 Ethical Use & Warnings

This tool is provided for authorized penetration testing, Bluetooth hardening assessments, and cybersecurity research only.

> ❌ NEVER use this in public, on strangers, or in illegal activities.




---

🛠️ Troubleshooting

Problem	Solution

rfcomm: can't connect	Target may have RFCOMM disabled or be out of range
Permission denied	Always run with sudo
obexftp not found	Install it with sudo apt install obexftp
No devices found	Move closer, make sure target is discoverable



---

📁 Folder Structure (Suggested)

bluetooth-attack-toolkit/
├── bt_attack.py
├── payload.txt
└── README.md


---

🧩 Coming Soon (Optional Features)

🔐 BLE (Bluetooth Low Energy) fuzzing

🧠 Auto-pairing & PIN brute force

⌨️ HID Keyboard injection module

📊 Logging and reporting module

🪪 GUI version using Tkinter



---

👨‍💻 Author

Built by [You] for educational use, inspired by APT simulation needs (e.g. Exbow Lite modules).


---
