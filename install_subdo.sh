#!/bin/bash

# SubDO Installation Script
# Created by wolf

echo "🚀 Installing SubDO - Subdomain Discovery Orchestrator..."
echo "🐺 Created by wolf"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Make the script executable
echo -e "${CYAN}📦 Setting up SubDO...${NC}"
chmod +x SubDO.py

# Create symlink for easy access
echo -e "${CYAN}🔗 Creating system-wide command...${NC}"
if sudo ln -sf "$(pwd)/SubDO.py" /usr/local/bin/subdo 2>/dev/null; then
    echo -e "${GREEN}✅ SubDO installed as 'subdo' command${NC}"
else
    echo -e "${YELLOW}⚠️  Could not create system-wide command (run with sudo or manually add to PATH)${NC}"
fi

# Check Python version
echo -e "${CYAN}🐍 Checking Python environment...${NC}"
python3 --version

# Install Python dependencies if needed
echo -e "${CYAN}📚 Installing Python dependencies...${NC}"
pip3 install --user concurrent.futures pathlib datetime argparse typing 2>/dev/null || echo -e "${YELLOW}⚠️  Some dependencies may already be installed${NC}"

# Check for reconnaissance tools
echo -e "${CYAN}🔍 Checking reconnaissance tools availability...${NC}"
echo ""

tools_to_check=(
    "subfinder:🔍 Fast passive subdomain enumeration"
    "assetfinder:🎯 Find domains and subdomains" 
    "amass:🔥 In-depth attack surface mapping"
    "bbot:🕷️ Recursive internet scanner"
    "ffuf:💨 Fast web fuzzer"
    "subwiz:🤖 ML-based subdomain prediction"
    "sudomy:⚡ Advanced subdomain analysis"
    "dnscan:🚀 Fast DNS brute force scanner"
    "subdog:🐕 Fast subdomain discovery"
)

available_tools=0
total_tools=${#tools_to_check[@]}

for tool_info in "${tools_to_check[@]}"; do
    tool=$(echo "$tool_info" | cut -d':' -f1)
    desc=$(echo "$tool_info" | cut -d':' -f2)
    
    if command -v "$tool" &> /dev/null; then
        echo -e "  ${GREEN}✅ $tool${NC} - $desc"
        ((available_tools++))
    else
        echo -e "  ${RED}❌ $tool${NC} - $desc"
    fi
done

echo ""
echo -e "${MAGENTA}📊 Arsenal Status: $available_tools/$total_tools tools available${NC}"

# Create wordlists directory
echo -e "${CYAN}📝 Setting up wordlists directory...${NC}"
mkdir -p ~/.subdo/wordlists
mkdir -p ~/.subdo/configs

# Download essential wordlists if they don't exist
if [ ! -f ~/.subdo/wordlists/subdomains-5000.txt ]; then
    echo -e "${CYAN}📥 Downloading essential wordlists...${NC}"
    curl -s https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-5000.txt -o ~/.subdo/wordlists/subdomains-5000.txt 2>/dev/null && echo -e "${GREEN}✅ Downloaded subdomains wordlist${NC}" || echo -e "${YELLOW}⚠️  Could not download wordlist${NC}"
fi

# Installation suggestions for missing tools
if [ $available_tools -lt $total_tools ]; then
    echo ""
    echo -e "${YELLOW}💡 Installation Guide for Missing Tools:${NC}"
    echo ""
    echo -e "${CYAN}For BlackArch/Arch Linux:${NC}"
    echo "  sudo pacman -S subfinder assetfinder amass ffuf"
    echo ""
    echo -e "${CYAN}For Ubuntu/Debian:${NC}"
    echo "  # Install Go first, then:"
    echo "  go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"
    echo "  go install github.com/tomnomnom/assetfinder@latest"
    echo "  go install github.com/owasp-amass/amass/v4/...@latest"
    echo "  go install github.com/ffuf/ffuf@latest"
    echo ""
    echo -e "${CYAN}Python/Pip tools:${NC}"
    echo "  pip install bbot subwiz"
    echo ""
    echo -e "${CYAN}Manual installations:${NC}"
    echo "  # Sudomy: git clone https://github.com/screetsec/Sudomy"
    echo "  # Dnscan: git clone https://github.com/rbsec/dnscan"
    echo "  # Subdog: git clone https://github.com/rix4uni/SubDog"
fi

# Create sample configuration file
echo -e "${CYAN}⚙️  Creating sample configuration...${NC}"
cat > ~/.subdo/configs/subdo_config.json << EOF
{
  "default_timeout": 300,
  "default_threads": 8,
  "wordlists": {
    "subdomains": "~/.subdo/wordlists/subdomains-5000.txt",
    "directories": "/usr/share/wordlists/dirb/common.txt"
  },
  "tool_preferences": {
    "passive_first": true,
    "skip_slow_tools": false
  }
}
EOF

# Test installation
echo ""
echo -e "${CYAN}🧪 Testing SubDO installation...${NC}"
if python3 SubDO.py --version 2>/dev/null; then
    echo -e "${GREEN}✅ SubDO is working correctly!${NC}"
else
    echo -e "${RED}❌ SubDO test failed${NC}"
fi

echo ""
echo -e "${GREEN}🎯 SubDO Installation Summary:${NC}"
echo -e "${GREEN}================================${NC}"
echo -e "📁 Installation Directory: $(pwd)"
echo -e "📋 Configuration Directory: ~/.subdo/"
echo -e "🔧 Available Tools: $available_tools/$total_tools"

if command -v subdo &> /dev/null; then
    echo -e "🚀 System Command: ${GREEN}subdo${NC} (ready to use)"
else
    echo -e "🚀 Direct Usage: ${GREEN}python3 SubDO.py${NC}"
fi

echo ""
echo -e "${MAGENTA}🚀 Usage Examples:${NC}"
echo -e "  ${GREEN}subdo -t example.com${NC}"
echo -e "  ${GREEN}subdo -t example.com --silent${NC}"  
echo -e "  ${GREEN}subdo -t example.com --tools subfinder amass --threads 12${NC}"
echo -e "  ${GREEN}python3 SubDO.py -t example.com --verbose${NC}"
echo ""
echo -e "${YELLOW}📚 Integration Examples:${NC}"
echo -e "  ${GRAY}# Check alive subdomains${NC}"
echo -e "  ${GREEN}httpx -l SubDO_*/all_subdomains_*.txt -o alive.txt${NC}"
echo ""
echo -e "  ${GRAY}# Run nuclei on discovered subdomains${NC}"  
echo -e "  ${GREEN}nuclei -l SubDO_*/all_subdomains_*.txt -t ~/nuclei-templates/${NC}"
echo ""
echo -e "${MAGENTA}🐺 SubDO by wolf - Ready for reconnaissance! 🚀${NC}"