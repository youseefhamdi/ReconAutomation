# Reconnaissance Tools Installation Guide

## Required Tools Installation

### 1. Subfinder
```bash
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```

### 2. AssetFinder
```bash
go install github.com/tomnomnom/assetfinder@latest
```

### 3. Amass
```bash
# Option 1: Go install
go install -v github.com/owasp-amass/amass/v4/...@master

# Option 2: Kali Linux
sudo apt install amass
```

### 4. BBOT
```bash
pip3 install bbot
```

### 5. FFUF
```bash
go install github.com/ffuf/ffuf/v2@latest
```

### 6. Subdog
```bash
# Install from GitHub
git clone https://github.com/guelfoweb/subdog.git
cd subdog
pip3 install -r requirements.txt
sudo cp subdog /usr/local/bin/
```

### 7. Sudomy
```bash
# Clone and install
git clone --recursive https://github.com/screetsec/Sudomy.git
cd Sudomy
pip3 install -r requirements.txt
sudo cp sudomy /usr/local/bin/
```

### 8. DNScan
```bash
git clone https://github.com/rbsec/dnscan.git
cd dnscan
pip3 install -r requirements.txt
sudo cp dnscan.py /usr/local/bin/dnscan
sudo chmod +x /usr/local/bin/dnscan
```

### 9. Other Required Tools
```bash
# Prips (for IP range enumeration)
sudo apt install prips

# JQ (for JSON parsing)
sudo apt install jq

# Dig, whois (usually pre-installed)
sudo apt install dnsutils whois
```

### 10. Wordlists
```bash
# SecLists
sudo apt install seclists

# Or manual install
git clone https://github.com/danielmiessler/SecLists.git
sudo mv SecLists /usr/share/wordlists/seclists
```

## Usage

### Advanced Script
```bash
chmod +x advanced_recon.sh
./advanced_recon.sh example.com
```

### Simple Script
```bash
chmod +x simple_recon.sh
./simple_recon.sh example.com
```

## Script Features

### Advanced Script Features:
- Parallel execution of tools
- Comprehensive error handling
- Organized directory structure
- Automated deduplication
- Intelligence gathering
- Reverse DNS lookups
- Detailed reporting
- Color-coded output

### Simple Script Features:
- Sequential execution (follows your exact workflow)
- Basic error handling
- Clean output organization
- Summary reporting
- Easy to modify

## Output Structure
```
recon_example.com_20231201_120000/
├── subdomains/
│   ├── subfinder.txt
│   ├── assetfinder.txt
│   ├── amass_passive.txt
│   ├── bbot.txt
│   ├── ffuf.txt
│   ├── subdog.txt
│   ├── sudomy.txt
│   └── dnscan.txt
├── intelligence/
│   ├── org_intel.txt
│   ├── asn_*.txt
│   ├── all_asn.txt
│   ├── whois_cidrs.txt
│   └── reverse_dns.txt
├── final/
│   └── all_subdomains.txt
└── summary.txt
```

## Troubleshooting

### Common Issues:
1. **Tool not found**: Ensure all tools are in your PATH
2. **Permission denied**: Make scripts executable with `chmod +x`
3. **Wordlist missing**: Install seclists or update wordlist paths
4. **Timeout errors**: Some tools may timeout on large domains (this is normal)

### Performance Tips:
1. Run on a VPS with good internet connection
2. Use API keys for better results (configure in tool configs)
3. Monitor system resources during execution
4. Consider running different phases separately for very large domains

## Customization

Both scripts can be easily customized:
- Modify wordlist paths
- Adjust timeout values
- Add/remove tools
- Change output formats
- Add custom filtering
