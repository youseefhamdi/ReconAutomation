#!/usr/bin/env python3
"""
SubDO - Subdomain Discovery Orchestrator
A powerful parallel reconnaissance tool for bug bounty hunters and penetration testers
Created by wolf
"""

import re
import sys
import argparse
import subprocess
import concurrent.futures
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    GRAY = '\033[90m'

def print_banner():
    """Display the SubDO banner with styling"""
    banner = f"""{Colors.RED}{Colors.BOLD}
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                                                                              ║
    ║    {Colors.CYAN}███████╗██╗   ██╗██████╗ ██████╗  ██████╗                           {Colors.RED}║
    ║    {Colors.CYAN}██╔════╝██║   ██║██╔══██╗██╔══██╗██╔═══██╗                          {Colors.RED}║
    ║    {Colors.CYAN}███████╗██║   ██║██████╔╝██║  ██║██║   ██║                          {Colors.RED}║
    ║    {Colors.CYAN}╚════██║██║   ██║██╔══██╗██║  ██║██║   ██║                          {Colors.RED}║
    ║    {Colors.CYAN}███████║╚██████╔╝██████╔╝██████╔╝╚██████╔╝                          {Colors.RED}║
    ║    {Colors.CYAN}╚══════╝ ╚═════╝ ╚═════╝ ╚═════╝  ╚═════╝                           {Colors.RED}║
    ║                                                                              ║
    ║            {Colors.YELLOW}🔍 𝐒𝐮𝐛𝐝𝐨𝐦𝐚𝐢𝐧 𝐃𝐢𝐬𝐜𝐨𝐯𝐞𝐫𝐲 𝐎𝐫𝐜𝐡𝐞𝐬𝐭𝐫𝐚𝐭𝐨𝐫 🔍{Colors.RED}                  ║
    ║                  {Colors.MAGENTA}🐺 𝗖𝗿𝗲𝗮𝘁𝗲𝗱 𝗯𝘆 𝘄𝗼𝗹𝗳 🐺{Colors.RED}                            ║
    ║                                                                              ║
    ║      {Colors.GREEN}⚡ Lightning Fast • Multi-Tool • Silent Mode • Comprehensive ⚡{Colors.RED}        ║
    ║                                                                              ║
    ╚══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}

"""
    print(banner)

class SubDO:
    """Main SubDO class for subdomain discovery orchestration"""
    
    def __init__(self, silent: bool = False, timeout: int = 300, threads: int = 8, verbose: bool = False):
        self.silent = silent
        self.timeout = timeout
        self.threads = threads
        self.verbose = verbose
        self.start_time = datetime.now()
        
        # Enhanced regex pattern for subdomain validation
        self.subdomain_pattern = re.compile(
            r'^([a-z0-9]([a-z0-9\-]{0,61}[a-z0-9])?\.)+[a-z]{2,}$', 
            re.IGNORECASE
        )
        
        # Tools configuration with enhanced commands and metadata
        self.tools = {
            "subfinder": {
                "cmd": ["subfinder", "-d", "TARGET", "-silent", "-all", "-recursive"],
                "description": "🔍 Fast passive subdomain enumeration",
                "category": "passive",
                "priority": 1,
                "timeout_multiplier": 1.0
            },
            "assetfinder": {
                "cmd": ["assetfinder", "--subs-only", "TARGET"],
                "description": "🎯 Find domains and subdomains",
                "category": "passive",
                "priority": 1,
                "timeout_multiplier": 0.8
            },
            "amass": {
                "cmd": ["amass", "enum", "-active", "-d", "TARGET", "-silent", "-brute"],
                "description": "🔥 In-depth attack surface mapping",
                "category": "active",
                "priority": 2,
                "timeout_multiplier": 2.0
            },
            "bbot": {
                "cmd": ["bbot", "-t", "TARGET", "-f", "subdomain-enum", "-s", "--output-dir", "/tmp/bbot_TARGET"],
                "description": "🕷️ Recursive internet scanner",
                "category": "active",
                "priority": 2,
                "timeout_multiplier": 1.5
            },
            "sudomy": {
                "cmd": ["sudomy", "-d", "TARGET", "-aI", "webanalyze", "-rS", "-dP", "-pS", "-tO", "-gW", "--httpx", "--dnsprobe", "-s"],
                "description": "⚡ Advanced subdomain analysis",
                "category": "comprehensive",
                "priority": 3,
                "timeout_multiplier": 2.5
            },
            "dnscan": {
                "cmd": ["python3", "/usr/share/dnscan/dnscan.py", "-d", "TARGET", "-t", "100", "-w", "/usr/share/wordlists/subdomains-5000.txt"],
                "description": "🚀 Fast DNS brute force scanner",
                "category": "bruteforce",
                "priority": 2,
                "timeout_multiplier": 1.8
            },
            "subwiz": {
                "cmd": ["subwiz", "-d", "TARGET"],
                "description": "🤖 ML-based subdomain prediction",
                "category": "ai",
                "priority": 3,
                "timeout_multiplier": 1.2
            },
            "subdog": {
                "cmd": ["subdog", "TARGET", "--all"],
                "description": "🐕 Fast subdomain discovery",
                "category": "passive",
                "priority": 1,
                "timeout_multiplier": 1.0
            },
            "ffuf": {
                "cmd": ["ffuf", "-w", "/usr/share/wordlists/dirb/common.txt", "-u", "https://TARGET/FUZZ", "-mc", "200,204,301,302,307,401,403,405", "-fs", "0", "-t", "50"],
                "description": "💨 Fast web fuzzer for directories",
                "category": "directory",
                "priority": 4,
                "timeout_multiplier": 1.5
            }
        }
        
        # Statistics tracking
        self.stats = {
            'tools_run': 0,
            'tools_successful': 0,
            'tools_failed': 0,
            'total_subdomains': 0,
            'unique_subdomains': 0,
            'execution_time': 0
        }

    def log(self, message: str, level: str = "INFO", force: bool = False):
        """Enhanced logging with emoji icons and timestamps"""
        if self.silent and not force:
            return
            
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Color and icon mapping
        level_config = {
            "INFO": {"color": Colors.CYAN, "icon": "ℹ️"},
            "SUCCESS": {"color": Colors.GREEN, "icon": "✅"},
            "WARNING": {"color": Colors.YELLOW, "icon": "⚠️"},
            "ERROR": {"color": Colors.RED, "icon": "❌"},
            "BANNER": {"color": Colors.MAGENTA, "icon": "🚀"},
            "DEBUG": {"color": Colors.GRAY, "icon": "🔧"}
        }
        
        config = level_config.get(level, {"color": Colors.WHITE, "icon": "📝"})
        
        if self.verbose or level != "DEBUG":
            print(f"{config['color']}[{timestamp}] {config['icon']} [{level}]{Colors.RESET} {message}")

    def check_tool_availability(self) -> Dict[str, Dict]:
        """Enhanced tool availability check with detailed analysis"""
        available_tools = {}
        categories = {}
        
        self.log("🔍 Scanning for available reconnaissance tools...", "INFO")
        
        for tool_name, tool_config in self.tools.items():
            try:
                cmd = tool_config["cmd"][0]
                
                # Try multiple methods to check tool availability
                check_commands = [
                    [cmd, "--help"],
                    [cmd, "-h"],
                    ["which", cmd],
                    ["command", "-v", cmd]
                ]
                
                tool_found = False
                for check_cmd in check_commands:
                    try:
                        result = subprocess.run(
                            check_cmd, 
                            capture_output=True, 
                            text=True, 
                            timeout=5
                        )
                        if result.returncode == 0:
                            tool_found = True
                            break
                    except:
                        continue
                
                if tool_found:
                    available_tools[tool_name] = tool_config
                    category = tool_config.get("category", "general")
                    
                    if category not in categories:
                        categories[category] = []
                    categories[category].append(tool_name)
                    
                    self.log(f"{tool_config['description']} ✓ Available", "SUCCESS")
                else:
                    self.log(f"{tool_name} ✗ Not found in PATH", "WARNING")
                    
            except Exception as e:
                self.log(f"{tool_name} ✗ Check failed: {str(e)}", "WARNING")
        
        # Display summary
        self.log(f"🎯 Arsenal Status: {len(available_tools)}/{len(self.tools)} tools available", "BANNER")
        
        # Show tools by category
        for category, tools in categories.items():
            self.log(f"📂 {category.upper()}: {', '.join(tools)}", "INFO")
        
        if not available_tools:
            self.log("❌ No reconnaissance tools found! Please install tools first.", "ERROR")
            self.print_installation_guide()
        
        return available_tools

    def print_installation_guide(self):
        """Print installation guide for missing tools"""
        if not self.silent:
            print(f"\n{Colors.YELLOW}📦 Installation Guide:{Colors.RESET}")
            print(f"\n{Colors.CYAN}BlackArch/Arch Linux:{Colors.RESET}")
            print("  sudo pacman -S subfinder assetfinder amass ffuf")
            print(f"\n{Colors.CYAN}Ubuntu/Debian:{Colors.RESET}")
            print("  # Install Go tools")
            print("  go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest")
            print("  go install github.com/tomnomnom/assetfinder@latest")
            print("  go install github.com/owasp-amass/amass/v4/...@latest")
            print("  go install github.com/ffuf/ffuf@latest")
            print(f"\n{Colors.CYAN}Python tools:{Colors.RESET}")
            print("  pip install bbot subwiz")

    def advanced_subdomain_filter(self, lines: List[str], tool_name: str) -> Tuple[List[str], List[str]]:
        """Advanced filtering with tool-specific patterns and validation"""
        subdomains = set()
        other_lines = []
        
        # Tool-specific noise patterns
        noise_patterns = {
            'amass': [
                'subdomain found:', '[info]', '[error]', 'enum', 'passive', 'active',
                'average:', 'dns queries', 'alterations', 'brute forcing', 'scraping'
            ],
            'sudomy': [
                'scanning', 'found', 'target:', 'results:', 'total:', 'webanalyze',
                'httpx', 'dnsprobe', 'checking', 'subdomain takeover'
            ],
            'bbot': [
                '[info]', '[debug]', '[warning]', '[error]', 'scan', 'module',
                'starting', 'finished', 'emitting', 'type='
            ],
            'subfinder': [
                '[inf]', '[wrn]', '[err]', '[dbg]', 'current configuration'
            ],
            'dnscan': [
                'scanning', 'found', 'threads:', 'wordlist:', 'dns server',
                'wildcards detected', 'progress'
            ],
            'ffuf': [
                'status:', 'size:', 'words:', 'lines:', 'duration:', 'headers'
            ]
        }
        
        # Global noise patterns
        global_noise = [
            'timestamp', 'server', 'timeout', 'resolver', 'query', 'lookup',
            'dns', 'http', 'https', 'certificate', 'ssl', 'tls', 'error',
            'warning', 'debug', 'info', 'trace', 'starting', 'finished',
            'complete', 'initializing', 'configuration', 'version'
        ]
        
        tool_patterns = noise_patterns.get(tool_name, [])
        all_patterns = global_noise + tool_patterns
        
        for line in lines:
            original_line = line.strip()
            if not original_line:
                continue
                
            cleaned_line = original_line.lower()
            
            # Skip lines containing noise patterns
            if any(pattern in cleaned_line for pattern in all_patterns):
                other_lines.append(original_line)
                continue
            
            # Extract potential subdomain from complex output
            potential_subdomain = cleaned_line.split()[0] if ' ' in cleaned_line else cleaned_line
            
            # Advanced cleaning for different output formats
            cleaners = ['|', '[', ']', '(', ')', '{', '}', ',', ';', '"', "'"]
            for cleaner in cleaners:
                if cleaner in potential_subdomain:
                    potential_subdomain = potential_subdomain.split(cleaner)[0]
            
            # Remove common prefixes and suffixes
            prefixes = ['http://', 'https://', 'www.', 'ftp://']
            for prefix in prefixes:
                if potential_subdomain.startswith(prefix):
                    potential_subdomain = potential_subdomain[len(prefix):]
            
            # Remove port numbers
            if ':' in potential_subdomain and tool_name != 'ffuf':
                potential_subdomain = potential_subdomain.split(':')[0]
            
            # Remove paths
            if '/' in potential_subdomain:
                potential_subdomain = potential_subdomain.split('/')[0]
            
            # Final validation and cleaning
            potential_subdomain = potential_subdomain.strip().lower()
            
            # Validate subdomain format
            if (potential_subdomain and 
                len(potential_subdomain) > 3 and 
                len(potential_subdomain) < 255 and
                self.subdomain_pattern.match(potential_subdomain) and
                '.' in potential_subdomain):
                
                subdomains.add(potential_subdomain)
            else:
                if original_line and len(original_line) > 5:
                    other_lines.append(original_line)
        
        return sorted(list(subdomains)), other_lines

    def run_tool(self, tool_name: str, tool_config: Dict, target: str) -> Dict:
        """Enhanced tool execution with dynamic timeout and better error handling"""
        # Calculate dynamic timeout based on tool priority
        dynamic_timeout = int(self.timeout * tool_config.get('timeout_multiplier', 1.0))
        
        # Prepare command with target substitution
        cmd = [part.replace("TARGET", target) for part in tool_config["cmd"]]
        
        self.stats['tools_run'] += 1
        start_time = time.time()
        
        try:
            self.log(f"🚀 Launching {tool_name} [{tool_config['category']}] -> {target}", "INFO")
            
            # Run tool with enhanced configuration
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=dynamic_timeout,
                stderr=subprocess.PIPE,
                env={'LANG': 'C', 'LC_ALL': 'C'}  # Ensure English output
            )
            
            execution_time = time.time() - start_time
            
            # Process stdout and stderr
            output_lines = []
            if result.stdout:
                output_lines.extend(result.stdout.splitlines())
            
            # Include useful stderr (non-error messages for some tools)
            if result.stderr and not self.silent:
                stderr_lines = result.stderr.splitlines()
                useful_stderr = [
                    line for line in stderr_lines 
                    if not any(noise in line.lower() for noise in ['error', 'warning', 'failed'])
                ]
                output_lines.extend(useful_stderr)
            
            # Filter and process results
            subdomains, other_output = self.advanced_subdomain_filter(output_lines, tool_name)
            
            self.stats['tools_successful'] += 1
            self.stats['total_subdomains'] += len(subdomains)
            
            self.log(
                f"🎯 {tool_name} completed: {len(subdomains)} subdomains in {execution_time:.1f}s", 
                "SUCCESS"
            )
            
            return {
                'tool': tool_name,
                'subdomains': subdomains,
                'other_output': other_output,
                'success': True,
                'execution_time': execution_time,
                'return_code': result.returncode,
                'description': tool_config.get('description', tool_name),
                'category': tool_config.get('category', 'unknown'),
                'priority': tool_config.get('priority', 1)
            }
            
        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            self.stats['tools_failed'] += 1
            self.log(f"⏰ {tool_name} timed out after {dynamic_timeout}s", "ERROR")
            
            return {
                'tool': tool_name, 
                'subdomains': [], 
                'other_output': [], 
                'success': False,
                'execution_time': execution_time,
                'error': 'timeout'
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.stats['tools_failed'] += 1
            self.log(f"💥 {tool_name} failed: {str(e)}", "ERROR")
            
            return {
                'tool': tool_name, 
                'subdomains': [], 
                'other_output': [], 
                'success': False,
                'execution_time': execution_time,
                'error': str(e)
            }

    def run_parallel_reconnaissance(self, target: str, selected_tools: Optional[List[str]] = None) -> Optional[Dict]:
        """Enhanced parallel reconnaissance with intelligent scheduling"""
        available_tools = self.check_tool_availability()
        
        if not available_tools:
            return None
        
        # Filter tools if specific ones are selected
        if selected_tools:
            available_tools = {
                k: v for k, v in available_tools.items() 
                if k in selected_tools
            }
            if not available_tools:
                self.log("❌ None of the specified tools are available!", "ERROR")
                return None
        
        self.log(f"🎯 Initiating parallel reconnaissance with {len(available_tools)} tools", "BANNER")
        
        # Sort tools by priority (lower number = higher priority)
        sorted_tools = sorted(
            available_tools.items(), 
            key=lambda x: x[1].get('priority', 1)
        )
        
        all_subdomains = set()
        tool_results = {}
        
        # Execute tools in parallel with thread pool
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
            # Submit all tools for execution
            future_to_tool = {
                executor.submit(self.run_tool, tool_name, tool_config, target): tool_name
                for tool_name, tool_config in sorted_tools
            }
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_tool):
                result = future.result()
                tool_name = result['tool']
                
                if result['success']:
                    all_subdomains.update(result['subdomains'])
                
                tool_results[tool_name] = result
        
        # Calculate final statistics
        total_execution_time = time.time() - self.start_time.timestamp()
        unique_subdomains = sorted(list(all_subdomains))
        
        self.stats['unique_subdomains'] = len(unique_subdomains)
        self.stats['execution_time'] = total_execution_time
        
        self.log(
            f"🏆 Reconnaissance complete! {self.stats['tools_successful']}/{len(available_tools)} tools successful", 
            "SUCCESS"
        )
        
        return {
            'target': target,
            'subdomains': unique_subdomains,
            'tool_results': tool_results,
            'statistics': self.stats.copy(),
            'scan_info': {
                'start_time': self.start_time.isoformat(),
                'end_time': datetime.now().isoformat(),
                'total_execution_time': total_execution_time,
                'threads_used': self.threads,
                'timeout_per_tool': self.timeout
            }
        }

    def save_comprehensive_results(self, scan_results: Dict) -> Path:
        """Enhanced results saving with comprehensive organization and analysis"""
        target = scan_results['target']
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create main output directory
        output_dir = Path(f"SubDO_{target}_{timestamp}")
        output_dir.mkdir(exist_ok=True, parents=True)
        
        # Create organized subdirectories
        subdirs = ["subdomains", "raw_outputs", "analysis", "metadata"]
        for subdir in subdirs:
            (output_dir / subdir).mkdir(exist_ok=True)
        
        # Save main comprehensive subdomain list
        main_file = output_dir / f"all_subdomains_{target}.txt"
        with main_file.open('w', encoding='utf-8') as f:
            f.write(f"# SubDO Comprehensive Subdomain Results\n")
            f.write(f"# Target: {target}\n")
            f.write(f"# Scan Date: {scan_results['scan_info']['start_time']}\n")
            f.write(f"# Total Subdomains: {len(scan_results['subdomains'])}\n")
            f.write(f"# Successful Tools: {scan_results['statistics']['tools_successful']}\n")
            f.write(f"# Execution Time: {scan_results['statistics']['execution_time']:.2f}s\n")
            f.write("# " + "="*70 + "\n\n")
            
            for i, subdomain in enumerate(scan_results['subdomains'], 1):
                f.write(f"{subdomain}\n")
        
        # Save individual tool results
        for tool_name, result in scan_results['tool_results'].items():
            if result['success'] and result['subdomains']:
                # Individual tool subdomains
                tool_file = output_dir / "subdomains" / f"{tool_name}_subdomains.txt"
                with tool_file.open('w', encoding='utf-8') as f:
                    f.write(f"# {result.get('description', tool_name)}\n")
                    f.write(f"# Category: {result.get('category', 'unknown')}\n")
                    f.write(f"# Execution Time: {result['execution_time']:.2f}s\n")
                    f.write(f"# Subdomains Found: {len(result['subdomains'])}\n")
                    f.write(f"# " + "="*50 + "\n\n")
                    
                    for subdomain in sorted(result['subdomains']):
                        f.write(f"{subdomain}\n")
                
                # Raw tool outputs (for debugging and manual analysis)
                if result['other_output']:
                    raw_file = output_dir / "raw_outputs" / f"{tool_name}_raw.txt"
                    with raw_file.open('w', encoding='utf-8') as f:
                        f.write(f"# Raw output from {tool_name}\n")
                        f.write(f"# " + "="*50 + "\n\n")
                        for line in result['other_output']:
                            f.write(f"{line}\n")
        
        # Save comprehensive analysis report
        self.create_analysis_report(scan_results, output_dir)
        
        # Save metadata and statistics
        self.save_scan_metadata(scan_results, output_dir)
        
        # Create summary JSON for automation
        self.create_json_summary(scan_results, output_dir)
        
        self.log(f"📁 Results saved to {output_dir}", "SUCCESS", force=True)
        return output_dir

    def create_analysis_report(self, scan_results: Dict, output_dir: Path):
        """Create detailed analysis report"""
        analysis_file = output_dir / "analysis" / "comprehensive_report.txt"
        
        with analysis_file.open('w', encoding='utf-8') as f:
            f.write("="*90 + "\n")
            f.write("           SUBDO COMPREHENSIVE RECONNAISSANCE REPORT\n")
            f.write("="*90 + "\n\n")
            
            # Executive Summary
            f.write("EXECUTIVE SUMMARY\n")
            f.write("-" * 50 + "\n")
            f.write(f"Target Domain: {scan_results['target']}\n")
            f.write(f"Scan Date: {scan_results['scan_info']['start_time']}\n")
            f.write(f"Total Execution Time: {scan_results['statistics']['execution_time']:.2f} seconds\n")
            f.write(f"Unique Subdomains Discovered: {len(scan_results['subdomains'])}\n")
            f.write(f"Tools Executed: {scan_results['statistics']['tools_run']}\n")
            f.write(f"Successful Tools: {scan_results['statistics']['tools_successful']}\n")
            f.write(f"Failed Tools: {scan_results['statistics']['tools_failed']}\n")
            success_rate = (scan_results['statistics']['tools_successful'] / scan_results['statistics']['tools_run']) * 100
            f.write(f"Success Rate: {success_rate:.1f}%\n\n")
            
            # Tool Performance Analysis
            f.write("TOOL PERFORMANCE ANALYSIS\n")
            f.write("-" * 50 + "\n")
            f.write(f"{'Tool':<15} {'Status':<10} {'Subdomains':<12} {'Time(s)':<8} {'Category':<12} {'Description'}\n")
            f.write("-" * 90 + "\n")
            
            for tool_name, result in scan_results['tool_results'].items():
                status = "SUCCESS" if result['success'] else "FAILED"
                subdomain_count = len(result['subdomains']) if result['success'] else 0
                exec_time = result.get('execution_time', 0)
                category = result.get('category', 'unknown')
                description = result.get('description', 'N/A')[:30]
                
                f.write(f"{tool_name:<15} {status:<10} {subdomain_count:<12} {exec_time:<8.1f} {category:<12} {description}\n")
            
            # Subdomain Analysis
            f.write(f"\n\nSUBDOMAIN ANALYSIS\n")
            f.write("-" * 50 + "\n")
            
            # Categorize subdomains by patterns
            patterns = {
                'www': [s for s in scan_results['subdomains'] if s.startswith('www.')],
                'api': [s for s in scan_results['subdomains'] if 'api' in s],
                'admin': [s for s in scan_results['subdomains'] if any(word in s for word in ['admin', 'manage', 'control'])],
                'dev': [s for s in scan_results['subdomains'] if any(word in s for word in ['dev', 'test', 'stage', 'staging'])],
                'mail': [s for s in scan_results['subdomains'] if any(word in s for word in ['mail', 'smtp', 'imap', 'pop'])],
                'cdn': [s for s in scan_results['subdomains'] if any(word in s for word in ['cdn', 'static', 'assets', 'media'])]
            }
            
            for pattern, subdomains in patterns.items():
                if subdomains:
                    f.write(f"{pattern.upper()} Subdomains ({len(subdomains)}): {', '.join(subdomains[:5])}")
                    if len(subdomains) > 5:
                        f.write(f" ... and {len(subdomains) - 5} more")
                    f.write("\n")
            
            # Complete subdomain list
            f.write(f"\n\nCOMPLETE SUBDOMAIN INVENTORY\n")
            f.write("-" * 50 + "\n")
            for i, subdomain in enumerate(scan_results['subdomains'], 1):
                f.write(f"{i:4}. {subdomain}\n")
        
        self.log(f"📊 Analysis report created: {analysis_file}", "INFO")

    def save_scan_metadata(self, scan_results: Dict, output_dir: Path):
        """Save scan metadata and configuration"""
        metadata_file = output_dir / "metadata" / "scan_metadata.json"
        
        metadata = {
            "subdo_version": "1.0.0",
            "scan_configuration": {
                "target": scan_results['target'],
                "threads": self.threads,
                "timeout": self.timeout,
                "silent_mode": self.silent,
                "verbose_mode": self.verbose
            },
            "scan_info": scan_results['scan_info'],
            "statistics": scan_results['statistics'],
            "tools_used": [
                {
                    "name": tool_name,
                    "success": result['success'],
                    "execution_time": result.get('execution_time', 0),
                    "subdomains_found": len(result['subdomains']) if result['success'] else 0,
                    "category": result.get('category', 'unknown')
                }
                for tool_name, result in scan_results['tool_results'].items()
            ]
        }
        
        with metadata_file.open('w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, default=str)

    def create_json_summary(self, scan_results: Dict, output_dir: Path):
        """Create JSON summary for automation and integration"""
        json_file = output_dir / f"subdomains_{scan_results['target']}.json"
        
        summary = {
            "target": scan_results['target'],
            "total_subdomains": len(scan_results['subdomains']),
            "scan_date": scan_results['scan_info']['start_time'],
            "execution_time": scan_results['statistics']['execution_time'],
            "subdomains": scan_results['subdomains'],
            "tools_summary": {
                tool_name: {
                    "success": result['success'],
                    "subdomains_count": len(result['subdomains']) if result['success'] else 0,
                    "execution_time": result.get('execution_time', 0)
                }
                for tool_name, result in scan_results['tool_results'].items()
            }
        }
        
        with json_file.open('w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)

    def display_final_summary(self, scan_results: Dict, output_dir: Path):
        """Display comprehensive final summary"""
        if self.silent:
            # In silent mode, just print the output directory
            print(str(output_dir))
            return
        
        # Beautiful completion banner
        print(f"\n{Colors.GREEN}{Colors.BOLD}")
        print("    ╔═════════════════════════════════════════════════════════════╗")
        print("    ║                  🎯 RECONNAISSANCE COMPLETE! 🎯            ║")
        print("    ╚═════════════════════════════════════════════════════════════╝")
        print(f"{Colors.RESET}")
        
        # Key metrics
        stats = scan_results['statistics']
        print(f"{Colors.CYAN}🎯 Target Domain:{Colors.RESET} {Colors.BOLD}{scan_results['target']}{Colors.RESET}")
        print(f"{Colors.CYAN}📊 Total Subdomains:{Colors.RESET} {Colors.BOLD}{Colors.GREEN}{len(scan_results['subdomains'])}{Colors.RESET}")
        print(f"{Colors.CYAN}⏱️  Execution Time:{Colors.RESET} {Colors.BOLD}{stats['execution_time']:.2f}s{Colors.RESET}")
        print(f"{Colors.CYAN}🛠️  Tools Used:{Colors.RESET} {Colors.BOLD}{stats['tools_successful']}/{stats['tools_run']}{Colors.RESET}")
        print(f"{Colors.CYAN}📁 Output Directory:{Colors.RESET} {output_dir}")
        
        # Tool performance table
        print(f"\n{Colors.YELLOW}🔧 Tool Performance Summary:{Colors.RESET}")
        print(f"{Colors.WHITE}{'Tool':<12} {'Status':<10} {'Subdomains':<10} {'Time':<8} {'Category'}{Colors.RESET}")
        print(f"{Colors.WHITE}{'-'*60}{Colors.RESET}")
        
        for tool_name, result in scan_results['tool_results'].items():
            status_color = Colors.GREEN if result['success'] else Colors.RED
            status_text = "✅ SUCCESS" if result['success'] else "❌ FAILED"
            subdomain_count = len(result['subdomains']) if result['success'] else 0
            exec_time = result.get('execution_time', 0)
            category = result.get('category', 'unknown')[:10]
            
            print(f"{Colors.WHITE}{tool_name:<12}{Colors.RESET} {status_color}{status_text:<10}{Colors.RESET} "
                  f"{Colors.BOLD}{subdomain_count:<10}{Colors.RESET} {exec_time:<8.1f} {category}")
        
        # Quick stats
        if len(scan_results['subdomains']) > 0:
            print(f"\n{Colors.MAGENTA}📈 Quick Analysis:{Colors.RESET}")
            patterns = {
                '🌐 WWW': len([s for s in scan_results['subdomains'] if s.startswith('www.')]),
                '🔌 API': len([s for s in scan_results['subdomains'] if 'api' in s]),
                '⚙️ ADMIN': len([s for s in scan_results['subdomains'] if any(word in s for word in ['admin', 'manage'])]),
                '🧪 DEV': len([s for s in scan_results['subdomains'] if any(word in s for word in ['dev', 'test', 'stage'])])
            }
            
            for pattern, count in patterns.items():
                if count > 0:
                    print(f"   {pattern}: {count} subdomains")
        
        # Final message
        print(f"\n{Colors.MAGENTA}{Colors.BOLD}🐺 SubDO by wolf - Happy Hunting! 🚀{Colors.RESET}")
        print(f"{Colors.GRAY}💡 Tip: Use 'httpx -l {output_dir}/all_subdomains_*.txt' to check alive subdomains{Colors.RESET}")

def main():
    """Main entry point with enhanced argument parsing"""
    parser = argparse.ArgumentParser(
        description='SubDO - Subdomain Discovery Orchestrator v1.0.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{Colors.CYAN}Examples:{Colors.RESET}
  {Colors.WHITE}python3 SubDO.py -t example.com{Colors.RESET}
  {Colors.WHITE}python3 SubDO.py -t example.com --silent{Colors.RESET}
  {Colors.WHITE}python3 SubDO.py -t example.com --tools subfinder amass --threads 12{Colors.RESET}
  {Colors.WHITE}python3 SubDO.py -t example.com --timeout 600 --verbose{Colors.RESET}

{Colors.YELLOW}Integration Examples:{Colors.RESET}
  {Colors.GRAY}# Check alive subdomains{Colors.RESET}
  {Colors.WHITE}httpx -l SubDO_*/all_subdomains_*.txt -o alive.txt{Colors.RESET}
  
  {Colors.GRAY}# Run nuclei on discovered subdomains{Colors.RESET}
  {Colors.WHITE}nuclei -l SubDO_*/all_subdomains_*.txt -t ~/nuclei-templates/{Colors.RESET}

{Colors.MAGENTA}Created by wolf 🐺{Colors.RESET}
        """
    )
    
    # Required arguments
    parser.add_argument(
        '-t', '--target', 
        required=True, 
        help='Target domain for reconnaissance (e.g., example.com)'
    )
    
    # Optional arguments
    parser.add_argument(
        '-s', '--silent', 
        action='store_true',
        help='Silent mode - minimal output, perfect for automation'
    )
    
    parser.add_argument(
        '--timeout', 
        type=int, 
        default=300,
        help='Base timeout per tool in seconds (default: 300)'
    )
    
    parser.add_argument(
        '--threads', 
        type=int, 
        default=8,
        help='Number of parallel threads (default: 8)'
    )
    
    parser.add_argument(
        '--tools', 
        nargs='+',
        help='Specific tools to use (default: all available)'
    )
    
    parser.add_argument(
        '--no-banner', 
        action='store_true',
        help='Skip banner display'
    )
    
    parser.add_argument(
        '--verbose', 
        action='store_true',
        help='Verbose output with debug information'
    )
    
    parser.add_argument(
        '--version', 
        action='version', 
        version='SubDO v1.0.0 - Created by wolf'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Validate target domain
    domain_pattern = re.compile(r'^([a-z0-9]([a-z0-9\-]{0,61}[a-z0-9])?\.)+[a-z]{2,}$', re.IGNORECASE)
    if not domain_pattern.match(args.target):
        print(f"{Colors.RED}❌ Invalid domain format: {args.target}{Colors.RESET}")
        sys.exit(1)
    
    # Display banner
    if not args.no_banner:
        print_banner()
    
    # Initialize SubDO
    try:
        subdo = SubDO(
            silent=args.silent,
            timeout=args.timeout,
            threads=args.threads,
            verbose=args.verbose
        )
        
        # Start reconnaissance
        subdo.log(f"🎯 Starting comprehensive reconnaissance for: {args.target}", "BANNER")
        
        results = subdo.run_parallel_reconnaissance(args.target, args.tools)
        
        if results:
            # Save comprehensive results
            output_dir = subdo.save_comprehensive_results(results)
            
            # Display final summary
            subdo.display_final_summary(results, output_dir)
            
        else:
            subdo.log("💥 Reconnaissance failed - no tools available", "ERROR")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️  Scan interrupted by user{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}💥 Fatal error: {str(e)}{Colors.RESET}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()