# Let me also create a simpler version and installation guide

simple_script = '''#!/bin/bash

# =============================================================================
# Simple Reconnaissance Automation Script
# Automates the exact tools and workflow requested by the user
# =============================================================================

# Colors
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
NC='\\033[0m'

# Configuration
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
WORDLIST="/usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt"

# Alternative wordlists if main one doesn't exist
if [ ! -f "$WORDLIST" ]; then
    WORDLIST="/usr/share/wordlists/dirb/common.txt"
fi

print_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Check if domain provided
if [ -z "$1" ]; then
    print_error "Usage: $0 <domain>"
    print_info "Example: $0 example.com"
    exit 1
fi

DOMAIN=$1
OUTPUT_DIR="recon_${DOMAIN}_${TIMESTAMP}"

# Create output structure
mkdir -p "$OUTPUT_DIR"/{subdomains,intelligence,final}

print_info "Starting reconnaissance for: $DOMAIN"
print_info "Output directory: $OUTPUT_DIR"

# 1. Subfinder
print_info "Running Subfinder..."
subfinder -d "$DOMAIN" -all --recursive -o "$OUTPUT_DIR/subdomains/subfinder.txt" -silent
print_success "Subfinder completed"

# 2. AssetFinder from targets.txt (create if doesn't exist)
print_info "Running AssetFinder..."
echo "$DOMAIN" > targets.txt
cat targets.txt | assetfinder -subs-only > "$OUTPUT_DIR/subdomains/assetfinder.txt"
print_success "AssetFinder completed"

# 3. Amass passive enumeration
print_info "Running Amass passive enumeration..."
amass enum -d "$DOMAIN" -o "$OUTPUT_DIR/subdomains/amass_passive.txt" 2>/dev/null
print_success "Amass passive enumeration completed"

# 4. BBOT (with timeout to prevent hanging)
print_info "Running BBOT..."
timeout 600 bbot -t "$DOMAIN" -p subdomain-enum cloud-enum code-enum email-enum spider web-basic paramminer dirbust-light web-screenshots --allow-deadly -o "$OUTPUT_DIR/bbot_output/" &>/dev/null || print_warning "BBOT completed with timeout"

# Extract subdomains from BBOT
find "$OUTPUT_DIR/bbot_output" -name "*.txt" -exec cat {} \\; 2>/dev/null | grep -E "\\.$DOMAIN$" | sort -u > "$OUTPUT_DIR/subdomains/bbot.txt" || touch "$OUTPUT_DIR/subdomains/bbot.txt"
print_success "BBOT completed"

# 5. FFUF subdomain fuzzing
if [ -f "$WORDLIST" ]; then
    print_info "Running FFUF subdomain fuzzing..."
    ffuf -w "$WORDLIST" -u "https://FUZZ.$DOMAIN" -mc 200,301,302,403 -o "$OUTPUT_DIR/subdomains/ffuf.json" -of json -s 2>/dev/null
    # Extract domains from JSON
    if [ -f "$OUTPUT_DIR/subdomains/ffuf.json" ]; then
        jq -r '.results[].url' "$OUTPUT_DIR/subdomains/ffuf.json" 2>/dev/null | sed 's|https\\?://||' | cut -d'/' -f1 > "$OUTPUT_DIR/subdomains/ffuf.txt"
    else
        touch "$OUTPUT_DIR/subdomains/ffuf.txt"
    fi
    print_success "FFUF completed"
else
    print_warning "No wordlist found for FFUF, skipping..."
    touch "$OUTPUT_DIR/subdomains/ffuf.txt"
fi

# 6. Subdog
print_info "Running Subdog..."
echo "$DOMAIN" | subdog -tools all > "$OUTPUT_DIR/subdomains/subdog.txt" 2>/dev/null || touch "$OUTPUT_DIR/subdomains/subdog.txt"
print_success "Subdog completed"

# 7. Sudomy
print_info "Running Sudomy..."
timeout 300 sudomy -d "$DOMAIN" --all -o "$OUTPUT_DIR/sudomy_out/" 2>/dev/null || print_warning "Sudomy completed with timeout"
find "$OUTPUT_DIR/sudomy_out" -name "*.txt" -exec cat {} \\; 2>/dev/null | sort -u > "$OUTPUT_DIR/subdomains/sudomy.txt" || touch "$OUTPUT_DIR/subdomains/sudomy.txt"
print_success "Sudomy completed"

# 8. DNScan
if [ -f "$WORDLIST" ]; then
    print_info "Running DNScan..."
    dnscan -d "$DOMAIN" -w "$WORDLIST" -o "$OUTPUT_DIR/subdomains/dnscan.txt" 2>/dev/null || touch "$OUTPUT_DIR/subdomains/dnscan.txt"
    print_success "DNScan completed"
else
    print_warning "No wordlist found for DNScan, skipping..."
    touch "$OUTPUT_DIR/subdomains/dnscan.txt"
fi

# Aggregate all subdomains
print_info "Aggregating all subdomains..."
cat "$OUTPUT_DIR"/subdomains/*.txt 2>/dev/null | grep -E "\\.$DOMAIN$" | sort -u > "$OUTPUT_DIR/final/all_subdomains.txt"
TOTAL_SUBS=$(wc -l < "$OUTPUT_DIR/final/all_subdomains.txt")
print_success "Found $TOTAL_SUBS unique subdomains"

# 9. Amass intel - organization
print_info "Running Amass intel for organization..."
ORG_NAME=$(echo "$DOMAIN" | cut -d'.' -f1)
amass intel -org "$ORG_NAME" -o "$OUTPUT_DIR/intelligence/org_intel.txt" 2>/dev/null || touch "$OUTPUT_DIR/intelligence/org_intel.txt"
print_success "Organization intelligence completed"

# 10. Amass intel - ASN (if org intel found ASNs)
if [ -s "$OUTPUT_DIR/intelligence/org_intel.txt" ]; then
    print_info "Running Amass intel for ASNs..."
    grep -oE 'AS[0-9]+' "$OUTPUT_DIR/intelligence/org_intel.txt" | head -5 | while read -r asn; do
        if [ ! -z "$asn" ]; then
            print_info "Processing ASN: $asn"
            amass intel -active -asn "$asn" -o "$OUTPUT_DIR/intelligence/asn_${asn}.txt" 2>/dev/null || true
        fi
    done
    
    # Combine ASN results
    cat "$OUTPUT_DIR/intelligence/asn_"*.txt > "$OUTPUT_DIR/intelligence/all_asn.txt" 2>/dev/null || touch "$OUTPUT_DIR/intelligence/all_asn.txt"
    print_success "ASN intelligence completed"
fi

# 11. Amass intel - CIDR (if ASN intel found CIDRs)
if [ -s "$OUTPUT_DIR/intelligence/all_asn.txt" ]; then
    print_info "Running Amass intel for CIDR ranges..."
    grep -oE "([0-9]{1,3}\\.){3}[0-9]{1,3}/[0-9]+" "$OUTPUT_DIR/intelligence/all_asn.txt" | head -3 | while read -r cidr; do
        if [ ! -z "$cidr" ]; then
            print_info "Processing CIDR: $cidr"
            amass intel -active -cidr "$cidr" -o "$OUTPUT_DIR/intelligence/cidr_${cidr//\\//_}.txt" 2>/dev/null || true
        fi
    done
    print_success "CIDR intelligence completed"
fi

# 12. WHOIS lookups for IP ranges
if [ -s "$OUTPUT_DIR/intelligence/all_asn.txt" ]; then
    print_info "Performing WHOIS lookups..."
    grep -oE 'AS[0-9]+' "$OUTPUT_DIR/intelligence/all_asn.txt" | head -3 | while read -r asn; do
        if [ ! -z "$asn" ]; then
            ASN_NUM=$(echo "$asn" | sed 's/AS//')
            whois -h whois.radb.net -- "-i origin AS$ASN_NUM" | grep -Eo "([0-9.]+){4}/[0-9]+" | sort -u >> "$OUTPUT_DIR/intelligence/whois_cidrs.txt" 2>/dev/null || true
        fi
    done
    print_success "WHOIS lookups completed"
fi

# 13. Reverse DNS lookups
if [ -s "$OUTPUT_DIR/intelligence/whois_cidrs.txt" ]; then
    print_info "Performing reverse DNS lookups..."
    head -3 "$OUTPUT_DIR/intelligence/whois_cidrs.txt" | while read -r cidr_range; do
        if [ ! -z "$cidr_range" ]; then
            print_info "Reverse DNS for: $cidr_range"
            prips "$cidr_range" 2>/dev/null | head -20 | while read -r ip; do
                reverse_result=$(dig -x "$ip" +short 2>/dev/null)
                if [ ! -z "$reverse_result" ] && [ "$reverse_result" != ";" ]; then
                    echo "$ip -> $reverse_result" >> "$OUTPUT_DIR/intelligence/reverse_dns.txt"
                fi
            done
        fi
    done
    print_success "Reverse DNS lookups completed"
fi

# Generate summary
cat > "$OUTPUT_DIR/summary.txt" << EOF
RECONNAISSANCE SUMMARY for $DOMAIN
=====================================
Generated: $(date)
Total Subdomains: $TOTAL_SUBS

Tool Results:
- Subfinder: $(wc -l < "$OUTPUT_DIR/subdomains/subfinder.txt" 2>/dev/null || echo 0)
- AssetFinder: $(wc -l < "$OUTPUT_DIR/subdomains/assetfinder.txt" 2>/dev/null || echo 0)
- Amass: $(wc -l < "$OUTPUT_DIR/subdomains/amass_passive.txt" 2>/dev/null || echo 0)
- BBOT: $(wc -l < "$OUTPUT_DIR/subdomains/bbot.txt" 2>/dev/null || echo 0)
- FFUF: $(wc -l < "$OUTPUT_DIR/subdomains/ffuf.txt" 2>/dev/null || echo 0)
- Subdog: $(wc -l < "$OUTPUT_DIR/subdomains/subdog.txt" 2>/dev/null || echo 0)
- Sudomy: $(wc -l < "$OUTPUT_DIR/subdomains/sudomy.txt" 2>/dev/null || echo 0)
- DNScan: $(wc -l < "$OUTPUT_DIR/subdomains/dnscan.txt" 2>/dev/null || echo 0)

Key Files:
- final/all_subdomains.txt: All unique subdomains
- intelligence/: Organization, ASN, and CIDR data
- intelligence/reverse_dns.txt: Reverse DNS results

Intelligence:
- Organization intel: $(wc -l < "$OUTPUT_DIR/intelligence/org_intel.txt" 2>/dev/null || echo 0) entries
- ASN intel: $(ls "$OUTPUT_DIR/intelligence/asn_"*.txt 2>/dev/null | wc -l || echo 0) ASNs processed
- Reverse DNS: $(wc -l < "$OUTPUT_DIR/intelligence/reverse_dns.txt" 2>/dev/null || echo 0) entries
EOF

print_success "Reconnaissance completed!"
print_info "Summary: $OUTPUT_DIR/summary.txt"
print_info "All subdomains: $OUTPUT_DIR/final/all_subdomains.txt"
print_info "Check $OUTPUT_DIR for all results"
'''

# Create the simple script
with open("simple_recon.sh", "w") as f:
    f.write(simple_script)

# Create installation guide
install_guide = '''# Reconnaissance Tools Installation Guide

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
'''

with open("INSTALLATION_GUIDE.md", "w") as f:
    f.write(install_guide)

print("Files created:")
print("✓ simple_recon.sh - Exact workflow you requested")
print("✓ advanced_recon.sh - Enhanced version with parallel execution")
print("✓ INSTALLATION_GUIDE.md - Complete setup instructions")