# SubDO - Subdomain Discovery Orchestrator

```
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                                                                              ║
    ║    ███████╗██╗   ██╗██████╗ ██████╗  ██████╗                           ║
    ║    ██╔════╝██║   ██║██╔══██╗██╔══██╗██╔═══██╗                          ║
    ║    ███████╗██║   ██║██████╔╝██║  ██║██║   ██║                          ║
    ║    ╚════██║██║   ██║██╔══██╗██║  ██║██║   ██║                          ║
    ║    ███████║╚██████╔╝██████╔╝██████╔╝╚██████╔╝                          ║
    ║    ╚══════╝ ╚═════╝ ╚═════╝ ╚═════╝  ╚═════╝                           ║
    ║                                                                              ║
    ║            🔍 𝐒𝐮𝐛𝐝𝐨𝐦𝐚𝐢𝐧 𝐃𝐢𝐬𝐜𝐨𝐯𝐞𝐫𝐲 𝐎𝐫𝐜𝐡𝐞𝐬𝐭𝐫𝐚𝐭𝐨𝐫 🔍                  ║
    ║                  🐺 𝗖𝗿𝗲𝗮𝘁𝗲𝗱 𝗯𝘆 𝘄𝗼𝗹𝗳 🐺                            ║
    ║                                                                              ║
    ║      ⚡ Lightning Fast • Multi-Tool • Silent Mode • Comprehensive ⚡        ║
    ║                                                                              ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
```

**SubDO** is the ultimate subdomain discovery orchestrator designed for bug bounty hunters, penetration testers, and security researchers. It seamlessly integrates 9+ reconnaissance tools, runs them in parallel, intelligently filters outputs (especially messy tools like Amass), and provides comprehensive reporting.

## 🚀 **Key Features**

- **⚡ Lightning Fast Parallel Execution** - Run all tools simultaneously with intelligent threading
- **🎯 Smart Filtering & Extraction** - Advanced regex patterns to clean messy tool outputs (especially Amass)
- **🔇 Perfect Silent Mode** - Clean, minimal output ideal for automation and scripting
- **🛠️ 9+ Integrated Tools** - All major reconnaissance tools in one unified interface
- **📊 Comprehensive Reporting** - Organized results with detailed analysis and performance metrics
- **🎨 Beautiful Interface** - Stunning banner and colored output for enhanced user experience
- **🔧 Highly Configurable** - Custom timeouts, thread counts, tool selection, and verbose modes
- **📁 Organized Output** - Structured directories with JSON summaries for easy integration

## 🛠️ **Integrated Reconnaissance Arsenal**

| Tool | Description | Category | Priority |
|------|-------------|----------|----------|
| **Subfinder** | 🔍 Fast passive subdomain enumeration | Passive | High |
| **Assetfinder** | 🎯 Find domains and subdomains | Passive | High |
| **Amass** | 🔥 In-depth attack surface mapping | Active | Medium |
| **BBot** | 🕷️ Recursive internet scanner | Active | Medium |
| **Sudomy** | ⚡ Advanced subdomain analysis | Comprehensive | Low |
| **Dnscan** | 🚀 Fast DNS brute force scanner | Bruteforce | Medium |
| **Subwiz** | 🤖 ML-based subdomain prediction | AI | Low |
| **Subdog** | 🐕 Fast subdomain discovery | Passive | High |
| **FFUF** | 💨 Fast web fuzzer for directories | Directory | Lowest |

## 📦 **Installation**

### Quick Installation
```bash
# Download SubDO
wget https://raw.githubusercontent.com/example/SubDO/main/SubDO.py
wget https://raw.githubusercontent.com/example/SubDO/main/install_subdo.sh

# Run installation script
chmod +x install_subdo.sh
./install_subdo.sh
```

### Manual Installation
```bash
# Make executable
chmod +x SubDO.py

# Create system-wide command (optional)
sudo ln -sf $(pwd)/SubDO.py /usr/local/bin/subdo

# Test installation
python3 SubDO.py --version
```

### Tool Dependencies

#### BlackArch/Arch Linux
```bash
sudo pacman -S subfinder assetfinder amass ffuf
```

#### Ubuntu/Debian
```bash
# Install Go tools
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/tomnomnom/assetfinder@latest
go install github.com/owasp-amass/amass/v4/...@latest
go install github.com/ffuf/ffuf@latest
```

#### Python Tools
```bash
pip install bbot subwiz
```

#### Manual Installations
```bash
# Sudomy
git clone https://github.com/screetsec/Sudomy

# Dnscan  
git clone https://github.com/rbsec/dnscan

# Subdog
git clone https://github.com/rix4uni/SubDog
```

## 🚀 **Usage**

### Basic Usage
```bash
# Run comprehensive reconnaissance
python3 SubDO.py -t example.com

# Using system-wide command
subdo -t example.com
```

### Advanced Usage
```bash
# Silent mode for automation
subdo -t example.com --silent

# Custom configuration
subdo -t example.com --timeout 600 --threads 12

# Specific tools only
subdo -t example.com --tools subfinder amass subwiz

# Verbose output with debug information
subdo -t example.com --verbose

# Skip banner (perfect for scripts)
subdo -t example.com --no-banner --silent
```

### Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--target` | `-t` | Target domain for reconnaissance | Required |
| `--silent` | `-s` | Silent mode with minimal output | False |
| `--timeout` | | Base timeout per tool in seconds | 300 |
| `--threads` | | Number of parallel threads | 8 |
| `--tools` | | Specific tools to use | All available |
| `--no-banner` | | Skip banner display | False |
| `--verbose` | | Verbose output with debug info | False |
| `--version` | | Show version information | - |

## 📁 **Output Structure**

SubDO creates highly organized output directories:

```
SubDO_example.com_20250909_091234/
├── all_subdomains_example.com.txt     # 🎯 Main results with metadata
├── subdomains_example.com.json        # 📊 JSON summary for automation
├── subdomains/                        # 📂 Individual tool results
│   ├── subfinder_subdomains.txt
│   ├── amass_subdomains.txt
│   ├── subwiz_subdomains.txt
│   └── ...
├── raw_outputs/                       # 📝 Raw tool outputs (for debugging)
│   ├── subfinder_raw.txt
│   ├── amass_raw.txt
│   └── ...
├── analysis/                          # 📈 Analysis and reports
│   └── comprehensive_report.txt
└── metadata/                          # ⚙️ Scan metadata
    └── scan_metadata.json
```

## 🎯 **Example Output**

```bash
$ subdo -t example.com

    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║    ███████╗██╗   ██╗██████╗ ██████╗  ██████╗                           ║
    ║            🔍 𝐒𝐮𝐛𝐝𝐨𝐦𝐚𝐢𝐧 𝐃𝐢𝐬𝐜𝐨𝐯𝐞𝐫𝐲 𝐎𝐫𝐜𝐡𝐞𝐬𝐭𝐫𝐚𝐭𝐨𝐫 🔍                  ║
    ║                  🐺 𝗖𝗿𝗲𝗮𝘁𝗲𝗱 𝗯𝘆 𝘄𝗼𝗹𝗳 🐺                            ║
    ╚══════════════════════════════════════════════════════════════════════════════╝

[09:12:34] ℹ️ [INFO] 🔍 Scanning for available reconnaissance tools...
[09:12:34] ✅ [SUCCESS] 🔍 Fast passive subdomain enumeration ✓ Available
[09:12:34] ✅ [SUCCESS] 🎯 Find domains and subdomains ✓ Available
[09:12:34] ✅ [SUCCESS] 🔥 In-depth attack surface mapping ✓ Available
[09:12:34] 🚀 [BANNER] 🎯 Arsenal Status: 8/9 tools available
[09:12:34] ℹ️ [INFO] 📂 PASSIVE: subfinder, assetfinder, subdog
[09:12:34] ℹ️ [INFO] 📂 ACTIVE: amass, bbot
[09:12:34] ℹ️ [INFO] 📂 AI: subwiz
[09:12:34] 🚀 [BANNER] 🎯 Initiating parallel reconnaissance with 8 tools
[09:12:34] ℹ️ [INFO] 🚀 Launching subfinder [passive] -> example.com
[09:12:34] ℹ️ [INFO] 🚀 Launching assetfinder [passive] -> example.com
[09:12:34] ℹ️ [INFO] 🚀 Launching amass [active] -> example.com
[09:12:45] ✅ [SUCCESS] 🎯 subfinder completed: 25 subdomains in 11.2s
[09:12:52] ✅ [SUCCESS] 🎯 assetfinder completed: 18 subdomains in 18.4s
[09:13:15] ✅ [SUCCESS] 🎯 amass completed: 42 subdomains in 41.7s
[09:13:22] ✅ [SUCCESS] 🎯 subwiz completed: 31 subdomains in 48.1s
[09:13:25] ✅ [SUCCESS] 🏆 Reconnaissance complete! 8/8 tools successful

    ╔═════════════════════════════════════════════════════════════╗
    ║                  🎯 RECONNAISSANCE COMPLETE! 🎯            ║
    ╚═════════════════════════════════════════════════════════════╝

🎯 Target Domain: example.com
📊 Total Subdomains: 127
⏱️  Execution Time: 51.3s
🛠️  Tools Used: 8/8
📁 Output Directory: SubDO_example.com_20250909_091325

🔧 Tool Performance Summary:
Tool         Status     Subdomains Time     Category
------------------------------------------------------------
subfinder    ✅ SUCCESS 25         11.2     passive
assetfinder  ✅ SUCCESS 18         18.4     passive
amass        ✅ SUCCESS 42         41.7     active
subwiz       ✅ SUCCESS 31         48.1     ai
bbot         ✅ SUCCESS 19         35.2     active
subdog       ✅ SUCCESS 14         22.8     passive

📈 Quick Analysis:
   🌐 WWW: 3 subdomains
   🔌 API: 12 subdomains
   ⚙️ ADMIN: 5 subdomains
   🧪 DEV: 8 subdomains

🐺 SubDO by wolf - Happy Hunting! 🚀
💡 Tip: Use 'httpx -l SubDO_*/all_subdomains_*.txt' to check alive subdomains
```

## 🔗 **Integration Examples**

### Check Alive Subdomains
```bash
# Run SubDO then check which subdomains are alive
subdo -t example.com --silent
httpx -l SubDO_*/all_subdomains_*.txt -o alive_subdomains.txt
```

### Vulnerability Scanning
```bash
# Run SubDO then scan for vulnerabilities
subdo -t example.com --silent
nuclei -l SubDO_*/all_subdomains_*.txt -t ~/nuclei-templates/ -o vulnerabilities.txt
```

### Directory Brute Forcing
```bash
# Run SubDO then brute force directories on alive subdomains
subdo -t example.com --silent
httpx -l SubDO_*/all_subdomains_*.txt | ffuf -w wordlist.txt -u FUZZ/FUZZ
```

### Automated Bug Bounty Workflow
```bash
#!/bin/bash
TARGET=$1

# Step 1: Comprehensive subdomain discovery
echo "🔍 Starting reconnaissance for $TARGET"
subdo -t $TARGET --silent

# Step 2: Get latest results directory
OUTPUT_DIR=$(ls -td SubDO_$TARGET_* | head -1)
SUBDOMAINS_FILE="$OUTPUT_DIR/all_subdomains_$TARGET.txt"

# Step 3: Check alive subdomains
echo "🌐 Checking alive subdomains"
httpx -l $SUBDOMAINS_FILE -o alive_$TARGET.txt

# Step 4: Screenshot alive subdomains
echo "📸 Taking screenshots"
gowitness file -f alive_$TARGET.txt

# Step 5: Run vulnerability scans
echo "🔍 Running vulnerability scans"
nuclei -l alive_$TARGET.txt -t ~/nuclei-templates/ -o vulns_$TARGET.txt

# Step 6: Directory brute forcing on main targets
echo "📂 Directory brute forcing"
cat alive_$TARGET.txt | head -10 | ffuf -w /usr/share/wordlists/dirb/common.txt -u FUZZ/FUZZ

echo "✅ Complete reconnaissance finished for $TARGET!"
echo "📁 Results: $(pwd)/$OUTPUT_DIR"
```

## 🛡️ **Advanced Features**

### Smart Output Filtering
SubDO includes advanced filtering specifically designed to handle messy outputs from tools like Amass:

```python
# Example of Amass raw output (messy):
# [09:12:34] Subdomain Found: api.example.com
# [09:12:35] FQDN: www.example.com [192.168.1.1]
# [09:12:36] DNS query timeout for test.example.com
# sub.example.com

# SubDO filtered output (clean):
# api.example.com  
# www.example.com
# sub.example.com
```

### Dynamic Timeout Management
Different tools have different timeout multipliers based on their complexity:
- **Fast tools** (Subfinder, Assetfinder): 1.0x base timeout
- **Medium tools** (Amass, BBot): 1.5-2.0x base timeout  
- **Comprehensive tools** (Sudomy): 2.5x base timeout

### Intelligent Tool Categorization
Tools are automatically categorized and can be filtered:
- **Passive**: subfinder, assetfinder, subdog
- **Active**: amass, bbot
- **Bruteforce**: dnscan
- **AI**: subwiz
- **Directory**: ffuf

### Performance Optimization
- **Parallel execution** with configurable thread pools
- **Memory-efficient** processing for large result sets
- **Progress tracking** with real-time status updates
- **Automatic cleanup** of temporary files

## 🚨 **Troubleshooting**

### Common Issues

1. **"No tools available" error**
   ```bash
   # Install missing tools
   sudo pacman -S subfinder assetfinder amass  # BlackArch
   go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest  # Manual
   ```

2. **Permission denied errors**
   ```bash
   chmod +x SubDO.py
   ```

3. **Timeout issues on slow networks**
   ```bash
   subdo -t example.com --timeout 600  # Increase timeout
   ```

4. **Memory issues with large targets**
   ```bash
   subdo -t example.com --threads 4  # Reduce thread count
   ```

5. **Tools hanging or not responding**
   ```bash
   subdo -t example.com --verbose  # Debug mode
   ```

### Debug Mode
```bash
# Run with single thread and verbose output for debugging
subdo -t example.com --threads 1 --verbose

# Test specific tools only
subdo -t example.com --tools subfinder --verbose
```

### Performance Tuning
```bash
# High-performance configuration
subdo -t example.com --threads 16 --timeout 180

# Conservative configuration for unstable networks
subdo -t example.com --threads 4 --timeout 900
```

## 📊 **Comparison with Other Tools**

| Feature | SubDO | Amass | Subfinder | Custom Scripts |
|---------|-------|-------|-----------|----------------|
| **Multiple Tools** | ✅ 9+ tools | ❌ Single | ❌ Single | ⚠️ Manual |
| **Parallel Execution** | ✅ Yes | ❌ No | ❌ No | ⚠️ Complex |
| **Smart Filtering** | ✅ Advanced | ⚠️ Basic | ✅ Good | ❌ None |
| **Silent Mode** | ✅ Perfect | ⚠️ Limited | ✅ Good | ❌ None |
| **Organized Output** | ✅ Comprehensive | ⚠️ Basic | ⚠️ Basic | ❌ Manual |
| **JSON Integration** | ✅ Built-in | ❌ No | ❌ No | ⚠️ Custom |
| **Error Handling** | ✅ Robust | ⚠️ Basic | ✅ Good | ❌ Manual |

## 🤝 **Contributing**

Contributions are welcome! Here's how you can help:

### Adding New Tools
1. Fork the repository
2. Add tool configuration to the `tools` dictionary
3. Test with various targets
4. Submit pull request

### Improving Filters
1. Identify tools with messy output
2. Add tool-specific filtering patterns
3. Test with real-world scenarios
4. Document changes

### Bug Reports
- Use the GitHub issue tracker
- Include full error messages
- Provide system information (OS, Python version, tool versions)
- Include sample commands that reproduce the issue

## 📜 **Changelog**

### v1.0.0 (2025-09-09)
- 🎉 Initial release with 9 integrated tools
- 🚀 Parallel execution engine with intelligent threading
- 🎯 Advanced filtering system for clean subdomain extraction
- 🎨 Beautiful banner and colored terminal output
- 📊 Comprehensive reporting with JSON summaries
- 🔇 Perfect silent mode for automation
- 🛠️ Dynamic timeout management
- 📁 Organized output structure
- ⚙️ Extensive configuration options

## 📄 **License**

This tool is created by **wolf** for educational and authorized security testing purposes only.

## ⚠️ **Disclaimer**

**SubDO** is intended for authorized security testing only. Users are responsible for complying with applicable laws and regulations. The author is not responsible for any misuse of this tool.

### Responsible Usage
- Only test domains you own or have explicit permission to test
- Respect rate limits and server resources
- Follow responsible disclosure practices
- Comply with bug bounty program rules and scope

---

**🐺 SubDO - Created by wolf | Happy Hunting! 🚀**

*The ultimate subdomain discovery orchestrator for security professionals.*