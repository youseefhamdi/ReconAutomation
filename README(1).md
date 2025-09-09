# 🔍 Advanced Reconnaissance Automation Suite

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Bash](https://img.shields.io/badge/bash-4.0%2B-brightgreen.svg)](https://www.gnu.org/software/bash/)
[![Platform](https://img.shields.io/badge/platform-linux-lightgrey.svg)](https://www.linux.org/)

A comprehensive reconnaissance automation suite designed for bug bounty hunters, penetration testers, and security researchers. This toolkit automates the complete reconnaissance workflow from subdomain enumeration to intelligence gathering and reverse DNS analysis.

## 🎯 Overview

The Advanced Reconnaissance Automation Suite integrates multiple industry-standard tools into a streamlined workflow, automating the tedious process of manual reconnaissance. Built with efficiency and accuracy in mind, it provides both parallel execution capabilities and sequential processing options to suit different use cases and system resources.

## ✨ Key Features

### 🚀 **Comprehensive Tool Integration**
- **Subfinder**: Passive subdomain discovery with 55+ data sources
- **AssetFinder**: Fast subdomain enumeration from various APIs
- **Amass**: Advanced OSINT framework with passive and active modules
- **BBOT**: Recursive web application security scanner
- **FFUF**: High-performance web fuzzer for subdomain discovery
- **Subdog**: Multiple tool integration wrapper
- **Sudomy**: Fast subdomain enumeration with various techniques
- **DNScan**: DNS subdomain scanner with wordlist support

### 🔧 **Advanced Automation Features**
- **Parallel Execution**: Simultaneous tool execution for maximum speed
- **Error Resilience**: Comprehensive error handling and recovery
- **Resource Management**: Intelligent job control and system resource monitoring
- **Progress Tracking**: Real-time status updates with color-coded output
- **Dependency Checking**: Automatic tool availability verification

### 📊 **Intelligence Gathering**
- **Organization Intelligence**: Corporate entity reconnaissance
- **ASN Enumeration**: Autonomous System Number analysis
- **CIDR Discovery**: IP range identification and mapping
- **Reverse DNS**: Bulk reverse DNS resolution
- **WHOIS Integration**: Automated domain and IP intelligence

### 📁 **Professional Output Management**
- **Organized Structure**: Systematic file organization with timestamps
- **Deduplication**: Automatic removal of duplicate subdomains
- **Aggregation**: Consolidated results from all tools
- **Detailed Reporting**: Comprehensive analysis and statistics
- **Export Formats**: Multiple output formats for further analysis

## 🛠️ Installation

### Prerequisites

Ensure you have the following installed on your system:
- **Operating System**: Linux (Ubuntu 20.04+ recommended)
- **Shell**: Bash 4.0 or higher
- **Go**: 1.19 or higher (for Go-based tools)
- **Python**: 3.8 or higher (for Python-based tools)
- **Git**: For cloning repositories

### Quick Install

```bash
# Clone the repository
git clone https://github.com/yourusername/recon-automation-suite.git
cd recon-automation-suite

# Make scripts executable
chmod +x *.sh

# Run the installation script
./install.sh
```

### Manual Installation

#### 1. Install Go-based Tools
```bash
# Subfinder
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# AssetFinder
go install github.com/tomnomnom/assetfinder@latest

# FFUF
go install github.com/ffuf/ffuf/v2@latest
```

#### 2. Install Python-based Tools
```bash
# BBOT
pip3 install bbot

# Install other Python dependencies
pip3 install requests dnspython colorama
```

#### 3. Install System Tools
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install amass prips dnsutils whois jq git curl

# Install Subdog
git clone https://github.com/guelfoweb/subdog.git
cd subdog && pip3 install -r requirements.txt
sudo cp subdog /usr/local/bin/

# Install Sudomy
git clone --recursive https://github.com/screetsec/Sudomy.git
cd Sudomy && pip3 install -r requirements.txt
sudo cp sudomy /usr/local/bin/

# Install DNScan
git clone https://github.com/rbsec/dnscan.git
cd dnscan && pip3 install -r requirements.txt
sudo cp dnscan.py /usr/local/bin/dnscan
```

#### 4. Install Wordlists
```bash
# SecLists (recommended)
sudo apt install seclists

# Or manual installation
git clone https://github.com/danielmiessler/SecLists.git
sudo mv SecLists /usr/share/wordlists/seclists
```

## 🚀 Usage

### Quick Start

```bash
# Basic usage with simple script
./simple_recon.sh example.com

# Advanced usage with parallel execution
./advanced_recon.sh example.com
```

### Script Options

#### Simple Script (simple_recon.sh)
- **Purpose**: Sequential execution following exact tool workflow
- **Best for**: Learning, debugging, resource-constrained environments
- **Features**: Basic error handling, clean output, easy modification

#### Advanced Script (advanced_recon.sh)
- **Purpose**: Parallel execution with advanced features
- **Best for**: Production use, large-scale reconnaissance, time-critical assessments
- **Features**: Parallel processing, comprehensive error handling, detailed reporting

### Configuration

#### Environment Variables
```bash
# Set custom wordlist path
export RECON_WORDLIST="/path/to/your/wordlist.txt"

# Set maximum parallel jobs (advanced script)
export MAX_PARALLEL_JOBS=15

# Set custom output directory
export RECON_OUTPUT_DIR="/path/to/output"
```

#### API Keys (Optional but Recommended)
Configure API keys for enhanced results:

```bash
# Subfinder API keys
echo 'shodan: ["your-shodan-api-key"]' > ~/.config/subfinder/provider-config.yaml
echo 'censys: ["your-censys-api-id:your-censys-secret"]' >> ~/.config/subfinder/provider-config.yaml

# Amass configuration
echo 'share = true' > ~/.config/amass/config.ini
echo '[data_sources.Shodan]' >> ~/.config/amass/config.ini
echo 'ttl = 1440' >> ~/.config/amass/config.ini
echo 'username =' >> ~/.config/amass/config.ini
echo 'password =' >> ~/.config/amass/config.ini
echo 'apikey = your-shodan-api-key' >> ~/.config/amass/config.ini
```

## 📂 Output Structure

```
recon_example.com_20231201_120000/
├── subdomains/                 # Individual tool outputs
│   ├── subfinder/
│   │   └── subfinder.txt
│   ├── assetfinder/
│   │   └── assetfinder.txt
│   ├── amass/
│   │   └── amass_passive.txt
│   ├── bbot/
│   │   └── bbot_subdomains.txt
│   ├── ffuf/
│   │   ├── ffuf.json
│   │   └── ffuf.txt
│   ├── subdog/
│   │   └── subdog.txt
│   ├── sudomy/
│   │   └── sudomy.txt
│   └── dnscan/
│       └── dnscan.txt
├── enumeration/                # Additional enumeration data
│   ├── live_hosts/
│   ├── technologies/
│   └── certificates/
├── intelligence/               # OSINT and intelligence data
│   ├── org_intel/
│   │   └── org_intel.txt
│   ├── asn_intel/
│   │   ├── asn_AS1234.txt
│   │   └── all_asn.txt
│   ├── cidr_intel/
│   │   └── cidr_results.txt
│   └── whois_data/
│       └── reverse_dns.txt
├── ports/                      # Port scanning results
├── screenshots/                # Web screenshots
├── reports/                    # Generated reports
│   └── reconnaissance_report.txt
├── wordlists/                  # Custom wordlists
├── raw_output/                 # Raw tool outputs
├── final_subdomains.txt        # Deduplicated final results
└── summary.txt                 # Executive summary
```

## 📊 Performance Metrics

### Tool Comparison

| Tool | Type | Speed | Sources | Quality | False Positives |
|------|------|-------|---------|---------|----------------|
| Subfinder | Passive | Fast | 55+ | High | Low |
| AssetFinder | Passive | Very Fast | 10+ | Medium | Medium |
| Amass | Passive/Active | Medium | 100+ | Very High | Very Low |
| BBOT | Active | Slow | 50+ | High | Low |
| FFUF | Active | Medium | Brute Force | Medium | High |
| Subdog | Passive | Fast | 20+ | Medium | Medium |
| Sudomy | Passive/Active | Medium | 30+ | High | Low |
| DNScan | Active | Fast | Brute Force | Medium | High |

### Expected Performance

| Domain Size | Runtime | Subdomains Found | Resources Used |
|-------------|---------|------------------|----------------|
| Small (< 100) | 5-10 min | 50-200 | 2 GB RAM |
| Medium (100-1000) | 10-30 min | 200-1500 | 3 GB RAM |
| Large (1000+) | 30+ min | 1500+ | 4+ GB RAM |

## 🔧 Advanced Configuration

### Custom Tool Integration

Add your own reconnaissance tools by modifying the script functions:

```bash
# Example: Adding a custom tool
run_custom_tool() {
    local domain=$1
    local output_dir=$2
    
    print_status "INFO" "Running Custom Tool on $domain..."
    your_custom_tool -d "$domain" -o "$output_dir/subdomains/custom/custom.txt"
    
    if [ -f "$output_dir/subdomains/custom/custom.txt" ]; then
        local count=$(wc -l < "$output_dir/subdomains/custom/custom.txt")
        print_status "SUCCESS" "Custom Tool found $count subdomains"
    fi
}
```

### Filtering and Processing

Customize subdomain filtering:

```bash
# Custom filtering in aggregate_subdomains function
grep -vE "(test|dev|staging)" "$output_dir/subdomains/all_subdomains_raw.txt" | \
    grep -E "^[a-zA-Z0-9][a-zA-Z0-9.-]*\.$domain$" | \
    sort -u > "$output_dir/subdomains/filtered_subdomains.txt"
```

## 🐛 Troubleshooting

### Common Issues

#### Tool Not Found
```bash
# Check if tool is in PATH
which subfinder
echo $PATH

# Install missing tools
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```

#### Permission Denied
```bash
# Make scripts executable
chmod +x *.sh

# Check file permissions
ls -la *.sh
```

#### Memory Issues
```bash
# Monitor system resources
htop

# Reduce parallel jobs
export MAX_PARALLEL_JOBS=5
```

#### Network Timeouts
```bash
# Increase timeout values in script
timeout 1200 bbot -t "$domain" ...

# Check network connectivity
ping google.com
```

### Debug Mode

Enable verbose output for troubleshooting:

```bash
# Run with debug enabled
DEBUG=1 ./advanced_recon.sh example.com

# Enable bash debugging
bash -x ./simple_recon.sh example.com
```

## 🔒 Security Considerations

### Rate Limiting
- Tools implement built-in rate limiting
- Consider using API keys to increase limits
- Monitor target responsiveness

### Legal and Ethical Use
- Only test domains you own or have explicit permission to test
- Respect robots.txt and security.txt files
- Follow responsible disclosure practices
- Comply with local laws and regulations

### OPSEC Considerations
- Use VPS or cloud instances for operational security
- Consider using VPNs or proxy chains
- Monitor and rotate IP addresses if needed
- Be aware of logging and attribution

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Submitting Issues
1. Check existing issues before creating new ones
2. Provide detailed reproduction steps
3. Include system information and tool versions
4. Add relevant logs and error messages

### Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with proper documentation
4. Test thoroughly on multiple systems
5. Commit with descriptive messages
6. Push to your fork and submit a pull request

### Code Standards
- Follow existing code style and formatting
- Add comments for complex logic
- Include error handling for new features
- Update documentation for any changes
- Test on multiple Linux distributions

## 📈 Roadmap

### Upcoming Features
- [ ] **Web Interface**: Browser-based dashboard for results
- [ ] **Database Integration**: PostgreSQL/MongoDB support for large datasets
- [ ] **API Endpoint**: REST API for programmatic access
- [ ] **Cloud Integration**: AWS/GCP/Azure deployment scripts
- [ ] **Machine Learning**: AI-powered subdomain validation
- [ ] **Real-time Updates**: Live monitoring and continuous reconnaissance
- [ ] **Mobile App**: Android/iOS companion app
- [ ] **Docker Support**: Containerized deployment options

### Tool Integrations
- [ ] **Nuclei Integration**: Automated vulnerability scanning
- [ ] **httpx Integration**: HTTP probing and technology detection
- [ ] **Naabu Integration**: Fast port scanning
- [ ] **Katana Integration**: Web crawling and spidering
- [ ] **Notify Integration**: Real-time notifications

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

### Tools and Projects
- [ProjectDiscovery](https://projectdiscovery.io/) - Subfinder, Nuclei, httpx
- [OWASP Amass](https://github.com/OWASP/Amass) - Advanced reconnaissance framework
- [Tom Hudson](https://github.com/tomnomnom) - AssetFinder and various security tools
- [FFUF](https://github.com/ffuf/ffuf) - Fast web fuzzer
- [BlackLanternSecurity](https://github.com/blacklanternsecurity/bbot) - BBOT framework

### Community
- Bug bounty community for methodology and best practices
- Security researchers for tool development and testing
- Open source contributors for continuous improvement

## 📞 Support

### Community Support
- **GitHub Issues**: [Create an issue](https://github.com/yourusername/recon-automation-suite/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/recon-automation-suite/discussions)
- **Discord**: [Join our community server](https://discord.gg/your-invite)

### Professional Support
For enterprise support, custom development, or training:
- **Email**: support@yourcompany.com
- **Website**: https://yourcompany.com

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/recon-automation-suite&type=Date)](https://star-history.com/#yourusername/recon-automation-suite&Date)

---

<div align="center">
<sub>Built with ❤️ for the cybersecurity community</sub>
</div>