# OS Fingerprinting CLI Tool

A visually engaging, interactive CLI tool for OS fingerprinting and basic network mapping – built for authorized penetration testers using Kali Linux.

---

## Features

- **Scan Modes:** Quick, Aggressive, and Custom (full nmap arg control)
- **Interactive CLI:** Target entry, scan mode selection, colorful menus
- **Nmap Integration:** Accurate OS detection using Nmap
- **Beautiful Output:** ASCII art, rich colors, and themed panels (via `rich` + `pyfiglet`)
- **3D Network Map:** Optional 3D visualization (requires matplotlib & networkx)
- **Configurable:** Settings via config file or CLI arguments
- **Error Handling:** Graceful on bad input/network errors
- **Ethical Warning:** Clear disclaimer at startup

---

## Installation

```bash
sudo apt update
sudo apt install python3-pip nmap
pip3 install rich pyfiglet
pip3 install matplotlib networkx  # (optional, for 3D map)
```

---

## Usage

```bash
python3 os_fingerprint_cli.py
```

### Workflow

1. **Disclaimer** – Reads and accepts the ethical warning.
2. **Target Selection** – Enter one or more IPs/hostnames (press Enter to finish).
3. **Scan Mode** – Choose scan mode (Quick, Aggressive, Custom).
4. **Scanning** – Nmap runs; results displayed with OS fingerprints.
5. **3D Map** – Optionally view a 3D network map (if matplotlib/networkx installed).

---

## Example Output

**Startup:**

```shell
 ____   _____       _____ _                               _       _   
/ __ \ / ____|     / ____| |                             | |     | |  
| |  | | (___   ___| (___ | |__   ___  _ __ ___ ___ _ __ | |_ ___| |_ 
| |  | |\___ \ / _ \\___ \| '_ \ / _ \| '__/ __/ _ \ '_ \| __/ _ \ __|
| |__| |____) |  __/____) | | | | (_) | | | (_|  __/ |_) | ||  __/ |_ 
\____/|_____/ \___|_____/|_| |_|\___/|_|  \___\___| .__/ \__\___|\__|
                                                | |                  
                                                |_|                  

╭────────────────────────── Ethical Disclaimer ─────────────────────────╮
│ WARNING: For authorized penetration testing only!                    │
│ Unauthorized use is illegal and unethical.                          │
╰──────────────────────────────────────────────────────────────────────╯

Welcome, penetration tester!

Enter target IP/hostname (leave blank to finish): 192.168.1.1
  Added: 192.168.1.1
Enter target IP/hostname (leave blank to finish):

Scan Modes
┏━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Option┃ Description                                                 ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 1     │ Quick: Fast scan (less accurate, stealthier)                │
│ 2     │ Aggressive: Thorough scan (more accurate, slower, noisy)    │
│ 3     │ Custom: Custom Nmap arguments                               │
└───────┴──────────────────────────────────────────────────────────────┘
Select scan mode [1-3]: 1

Selected scan mode: quick
Nmap args: -O --osscan-guess --max-retries 1 --host-timeout 30s

Scanning 192.168.1.1...

╭──────────────────── 192.168.1.1 ────────────────────╮
│ 192.168.1.1                                         │
│ Linux 4.15 - 5.6 (likely)                           │
╰─────────────────────────────────────────────────────╯

Scan complete. Stay ethical!
```

---

## Dependencies

- `python3`
- `rich`
- `pyfiglet`
- `nmap` (system binary)
- `matplotlib`, `networkx` (optional for 3D map)

---

## Ethical Use

> **WARNING:**  
> This tool is **strictly for authorized penetration testing** and research.  
> Unauthorized scanning is illegal and unethical.

---

## License

MIT
