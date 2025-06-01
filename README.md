# boom
boom is a Python-based automated reconnaissance tool for penetration testers and ethical hackers. It chains together powerful tools like **Nmap**, **Dirb**, and **FFUF** to perform efficient and fast target scanning with minimal manual input.

## 🚀 What It Does

Just run:
```bash
boom <ip-or-domain>
```

And BoomRecon will:

1. Perform an **aggressive Nmap scan**: `nmap -T5 -A <target>`
   - Saves open ports and service versions to `nmap.txt`.

2. Run a **Dirb directory brute-force scan**: `dirb http://<target>/`
   - Extracts only successful paths to `directory.txt`.

3. Conduct a **full port scan**: `nmap -T5 -A -p- <target>`
   - Appends newly discovered ports to `nmap.txt`.

4. Run **SYN** and **ACK scans**:
   - `nmap -sS <target>` and `nmap -sA <target>`
   - Appends any additional results to `nmap.txt`.

5. If the target is a domain (not an IP), it performs a **subdomain scan using FFUF**:
   - Saves results to `subdomains.json`.

Throughout the process, BoomRecon will update you with clear status messages (e.g., "TCP scan finished", "Dirb scan complete", etc.).

---

## 📁 Output Files

All results are saved inside the `boom_results/` directory:

- `nmap.txt`: All port/service scan results
- `directory.txt`: Valid directories from Dirb
- `subdomains.json`: Discovered subdomains (if applicable)

---

## ⚙️ Requirements

- Python 3.x
- The following tools must be installed and in your system PATH:
  - [`nmap`](https://nmap.org/)
  - [`dirb`](https://tools.kali.org/web-applications/dirb)
  - [`ffuf`](https://github.com/ffuf/ffuf)

You also need valid wordlists for:
- Subdomain brute-forcing (`SUBDOMAIN_WORDLIST`)
- Directory brute-forcing (`DIRB_WORDLIST`)

These paths can be set at the top of the Python script.

---

## 🔧 Setup

1. Clone the repo or save the script as `boom.py`.
2. Set your wordlist paths at the top of the script.
3. Make it executable (optional):
   ```bash
   chmod +x boom.py
   ```
4. Run it:
   ```bash
   python3 boom.py <target>
   ```

To make `boom` a terminal command, create a shell alias:
```bash
alias boom='python3 /full/path/to/boom.py'
```

---

## 📌 Notes

- Designed for Linux environments (Kali, Parrot OS, etc.)
- Intended for ethical use only — always get authorization before scanning!
- Add extra scan types or fingerprinting methods as needed.

---

## 🧠 TODO (Future Improvements)

- Colorized console output with `colorama`
- Error handling and dependency checks
- HTTP vs HTTPS auto-detection
- `argparse` support for custom options
- Multithreaded scanning (parallel tasks)

---

## 🛡️ Legal Disclaimer

This tool is intended **only for educational and authorized penetration testing** purposes. Unauthorized use of this tool on networks you do not own or have explicit permission to test may violate laws and regulations.

---

## 👨‍💻 Author

boom by @coduronin
Feel free to fork and contribute!
# boom
