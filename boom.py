import subprocess
import re
import os
from datetime import datetime

# === CONFIGURATION ===
SUBDOMAIN_WORDLIST = "/path/to/subdomains.txt"
DIRB_WORDLIST = "/usr/share/wordlists/dirb/common.txt"
OUTPUT_DIR = "boom_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_command(cmd, label=None):
    if label:
        print(f"[*] {label}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

def short_nmap_summary(nmap_output):
    open_ports = []
    for line in nmap_output.splitlines():
        if re.search(r"\d+/tcp\s+open", line):
            open_ports.append(line.strip())
    return "\n".join(open_ports)

def save_to_file(filename, content, mode="w"):
    with open(os.path.join(OUTPUT_DIR, filename), mode) as f:
        f.write(content + "\n")

def boom(ip):
    print(f"[+] Starting recon on {ip}")
    
    # 1. Basic aggressive scan
    nmap_cmd = f"nmap -T5 -A {ip}"
    output = run_command(nmap_cmd, "Running aggressive scan")
    summary = short_nmap_summary(output)
    save_to_file("nmap.txt", f"# Aggressive scan\n{summary}")
    print("[+] Initial Nmap scan complete.\n")

    # 2. Dirb scan
    dirb_cmd = f"dirb http://{ip}/ {DIRB_WORDLIST}"
    dirb_output = run_command(dirb_cmd, "Running Dirb")
    successful_dirs = "\n".join(
        re.findall(r"(http://[^\s]+)", dirb_output)
    )
    save_to_file("directory.txt", successful_dirs)
    print("[+] Dirb scan complete.\n")

    # 3. Full port scan
    nmap_full_cmd = f"nmap -T5 -A -p- {ip}"
    full_output = run_command(nmap_full_cmd, "Running full port scan")
    new_ports = short_nmap_summary(full_output)
    save_to_file("nmap.txt", f"# Full port scan\n{new_ports}", mode="a")
    print("[+] Full Nmap scan complete.\n")

    # 4. SYN scan
    syn_cmd = f"nmap -sS {ip}"
    syn_output = run_command(syn_cmd, "Running SYN scan")
    syn_ports = short_nmap_summary(syn_output)
    save_to_file("nmap.txt", f"# SYN scan\n{syn_ports}", mode="a")

    # 5. ACK scan
    ack_cmd = f"nmap -sA {ip}"
    ack_output = run_command(ack_cmd, "Running ACK scan")
    ack_ports = short_nmap_summary(ack_output)
    save_to_file("nmap.txt", f"# ACK scan\n{ack_ports}", mode="a")

    print("[+] TCP scan series finished.\n")

    # 6. FFUF for subdomains (assuming target is domain not IP)
    if not re.match(r"\d+\.\d+\.\d+\.\d+", ip):  # Check if it's not an IP
        ffuf_cmd = f"ffuf -u http://FUZZ.{ip} -w {SUBDOMAIN_WORDLIST} -t 30 -o {OUTPUT_DIR}/subdomains.json -of json"
        run_command(ffuf_cmd, "Running FFUF subdomain scan")
        print("[+] FFUF subdomain scan complete.")

    print(f"\n[✓] Boom recon completed. Results saved to: {OUTPUT_DIR}/")

# Example usage
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: boom <ip/domain>")
    else:
        boom(sys.argv[1])
