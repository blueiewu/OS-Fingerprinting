#!/usr/bin/env python3
"""
OS Fingerprinting Tool for Kali Linux
Author: blueiewu
Description: CLI-based OS fingerprinting tool leveraging Nmap,
with interactive menus, colorful visuals, and optional 3D network visualization.
"""

import os
import sys
import subprocess
import socket
import re
import configparser
from typing import List, Dict, Optional

try:
    import rich
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt
    from rich.text import Text
    from rich.theme import Theme
    from rich.progress import Progress
    from rich.style import Style
except ImportError:
    print("[!] Please install the 'rich' library: pip install rich")
    sys.exit(1)

try:
    import pyfiglet
except ImportError:
    print("[!] Please install the 'pyfiglet' library: pip install pyfiglet")
    sys.exit(1)

# Optional 3D Network Map
try:
    import networkx as nx
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    HAS_3D = True
except ImportError:
    HAS_3D = False

# ============ Global Config & Theme ============ #

CONFIG_PATH = "osfp_config.ini"
CUSTOM_THEME = Theme({
    "primary": "bold cyan",
    "danger": "bold red",
    "warning": "yellow",
    "success": "bold green",
    "info": "cyan",
    "scanmode": "magenta",
    "os": "bold blue",
    "ip": "bold white",
    "ascii": "bold green",
    "disclaimer": "bold yellow",
})

console = Console(theme=CUSTOM_THEME)

# ============ ASCII Art ============ #

def print_ascii_title():
    art = pyfiglet.figlet_format("OS FINGERPRINT", font="slant")
    console.print(art, style="ascii")

def print_disclaimer():
    panel = Panel(
        Text(
            "WARNING: For authorized penetration testing only!\n"
            "Unauthorized use is illegal and unethical.",
            style="disclaimer"
        ),
        title="Ethical Disclaimer",
        border_style="danger"
    )
    console.print(panel)

# ============ Config Handling ============ #

def load_config(path: str = CONFIG_PATH):
    config = configparser.ConfigParser()
    if os.path.exists(path):
        config.read(path)
    else:
        config["DEFAULT"] = {
            "nmap_path": "nmap",
            "default_scanmode": "quick"
        }
        with open(path, "w") as f:
            config.write(f)
    return config

# ============ Target Selection ============ #

def resolve_host(target: str) -> Optional[str]:
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        return None

def interactive_target_selection() -> List[str]:
    targets = []
    while True:
        target = Prompt.ask("[primary]Enter target IP/hostname (leave blank to finish)", default="")
        if not target.strip():
            break
        ip = resolve_host(target.strip())
        if ip:
            targets.append(ip)
            console.print(f"  [success]Added:[/success] [ip]{ip}[/ip]")
        else:
            console.print(f"  [danger]Invalid target: {target}[/danger]")
    return targets

# ============ Scan Modes ============ #

SCAN_MODES = {
    "quick": {
        "desc": "Fast scan (less accurate, stealthier)",
        "args": "-O --osscan-guess --max-retries 1 --host-timeout 30s"
    },
    "aggressive": {
        "desc": "Thorough scan (more accurate, slower, noisy)",
        "args": "-O -T4 --osscan-guess --version-all --max-retries 3"
    },
    "custom": {
        "desc": "Custom Nmap arguments"
    }
}

def select_scan_mode() -> (str, str):
    table = Table(title="Scan Modes", show_header=True, header_style="bold magenta")
    table.add_column("Option", style="scanmode", justify="center")
    table.add_column("Description")
    for idx, (mode, info) in enumerate(SCAN_MODES.items(), 1):
        table.add_row(str(idx), f"[primary]{mode.capitalize()}[/primary]: {info['desc']}")
    console.print(table)
    while True:
        choice = Prompt.ask(
            "[primary]Select scan mode [1-3][/primary]", choices=["1", "2", "3"], default="1"
        )
        if choice == "1":
            return "quick", SCAN_MODES["quick"]["args"]
        elif choice == "2":
            return "aggressive", SCAN_MODES["aggressive"]["args"]
        elif choice == "3":
            custom_args = Prompt.ask(
                "[scanmode]Enter your custom Nmap arguments (excluding target IP)[/scanmode]",
                default="-O"
            )
            return "custom", custom_args

# ============ Nmap Integration ============ #

def run_nmap_scan(nmap_path: str, targets: List[str], nmap_args: str) -> Dict[str, str]:
    results = {}
    for target in targets:
        console.print(f"\n[info]Scanning {target}...[/info]", style="info")
        cmd = f"{nmap_path} {nmap_args} {target}"
        try:
            with Progress() as progress:
                task = progress.add_task(f"[cyan]Nmap: {target}[/cyan]", total=100)
                proc = subprocess.run(
                    cmd.split(), capture_output=True, text=True, timeout=120
                )
                progress.update(task, advance=100)
            output = proc.stdout + proc.stderr
            results[target] = output
            if proc.returncode != 0:
                console.print(
                    f"[danger]Nmap returned error ({proc.returncode}) for {target}[/danger]\n{proc.stderr}",
                    style="danger"
                )
        except subprocess.TimeoutExpired:
            console.print(f"[danger]Scan timed out for {target}[/danger]", style="danger")
            results[target] = ""
    return results

# ============ OS Fingerprint Parsing ============ #

def parse_os_fingerprint(nmap_output: str) -> str:
    if not nmap_output:
        return "[danger]No output received[/danger]"
    # Find OS details in Nmap output
    os_match = re.findall(r"OS details: (.+)", nmap_output)
    os_guess = re.findall(r"Running: (.+)", nmap_output)
    if os_match:
        return f"[os]{os_match[0]}[/os]"
    elif os_guess:
        return f"[os]{os_guess[0]}[/os]"
    elif "No exact OS matches" in nmap_output:
        return "[warning]No exact OS match found[/warning]"
    elif "Too many fingerprints match" in nmap_output:
        return "[warning]Too many fingerprints matched[/warning]"
    elif "OS detection performed" in nmap_output:
        return "[warning]OS detection performed, but inconclusive[/warning]"
    else:
        return "[danger]Could not parse OS fingerprint[/danger]"

# ============ 3D Network Map (Optional) ============ #

def plot_3d_network_map(fingerprints: Dict[str, str]):
    if not HAS_3D:
        console.print(
            "[warning]3D map feature unavailable. Install matplotlib & networkx for 3D maps.[/warning]",
            style="warning"
        )
        return
    G = nx.Graph()
    for ip, osinfo in fingerprints.items():
        G.add_node(ip, label=osinfo)
    # Simple fake topology: all nodes connected to a "You" node
    G.add_node("You", label="Pentester")
    for ip in fingerprints:
        G.add_edge("You", ip)
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    pos = nx.spring_layout(G, dim=3, seed=42)
    xs, ys, zs = [], [], []
    for node in G.nodes():
        x, y, z = pos[node]
        xs.append(x)
        ys.append(y)
        zs.append(z)
        ax.text(x, y, z, f"{node}\n{G.nodes[node]['label']}", color='blue', fontsize=10)
    ax.scatter(xs, ys, zs, c='green', s=100)
    for edge in G.edges():
        x = [pos[edge[0]][0], pos[edge[1]][0]]
        y = [pos[edge[0]][1], pos[edge[1]][1]]
        z = [pos[edge[0]][2], pos[edge[1]][2]]
        ax.plot(x, y, z, c='grey')
    ax.set_title("3D Network Map")
    plt.show()

# ============ Main CLI ============ #

def main():
    print_ascii_title()
    print_disclaimer()
    config = load_config()
    nmap_path = config["DEFAULT"].get("nmap_path", "nmap")
    
    # Menu
    console.print("[primary]Welcome, penetration tester![/primary]", style="primary")
    targets = interactive_target_selection()
    if not targets:
        console.print("[danger]No targets provided. Exiting.[/danger]", style="danger")
        sys.exit(1)
    scanmode, nmap_args = select_scan_mode()
    console.print(f"[info]Selected scan mode: [scanmode]{scanmode}[/scanmode][/info]\n[info]Nmap args: {nmap_args}[/info]", style="info")

    # Scan
    results = run_nmap_scan(nmap_path, targets, nmap_args)
    fingerprints = {}
    for target, output in results.items():
        osinfo = parse_os_fingerprint(output)
        fingerprints[target] = osinfo
        panel = Panel.fit(
            Text(f"{target}\n{osinfo}", style="success"),
            title=f"[ip]{target}[/ip]",
            border_style="primary"
        )
        console.print(panel)

    # 3D Map Option
    if HAS_3D and Prompt.ask("[primary]Show 3D network map? (y/n)[/primary]", choices=["y", "n"], default="n") == "y":
        plot_3d_network_map(fingerprints)

    console.print("[success]Scan complete. Stay ethical![/success]", style="success")

# ============ Entrypoint ============ #

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[warning]Aborted by user.[/warning]", style="warning")
    except Exception as e:
        console.print(f"[danger]Error: {e}[/danger]", style="danger")