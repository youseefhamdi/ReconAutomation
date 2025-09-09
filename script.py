# Let me create a comprehensive bash script that automates the reconnaissance workflow
# Based on the user's requirements and best practices from the research

script_content = '''#!/bin/bash

# =============================================================================
# Advanced Reconnaissance Automation Script
# Author: Cybersecurity Automation
# Description: Comprehensive reconnaissance workflow automation
# =============================================================================

# Color codes for output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
PURPLE='\\033[0;35m'
CYAN='\\033[0;36m'
NC='\\033[0m' # No Color

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
MAX_PARALLEL_JOBS=10

# Function to print banner
print_banner() {
    echo -e "${CYAN}"
    echo "  ____                      ___        _                        _   _             "
    echo " |  _ \\ ___  ___ ___  _ __  / \\ _   _ | |_ ___  _ __ ___   __ _ | |_(_) ___  _ __  "
    echo " | |_) / _ \\/ __/ _ \\| '_ \\/  _\`| | | || __/ _ \\| '_ \` _ \\ / _\` || __| |/ _ \\| '_ \\ "
    echo " |  _ <  __/ (_| (_) | | | / ___ \\\\ |_| || || (_) | | | | | | (_| || |_| | (_) | | | |"
    echo " |_| \\_\\___|\\___\\___/|_| |_/_/   \\_\\\\__,_| \\__\\___/|_| |_| |_|\\__,_| \\__|_|\\___/|_| |_|"
    echo ""
    echo "                    Advanced Reconnaissance Automation v2.0"
    echo -e "${NC}"
}

# Function to print colored output
print_status() {
    local level=$1
    local message=$2
    case $level in
        "INFO")
            echo -e "${BLUE}[INFO]${NC} $message"
            ;;
        "SUCCESS")
            echo -e "${GREEN}[SUCCESS]${NC} $message"
            ;;
        "WARNING")
            echo -e "${YELLOW}[WARNING]${NC} $message"
            ;;
        "ERROR")
            echo -e "${RED}[ERROR]${NC} $message"
            ;;
        "PHASE")
            echo -e "${PURPLE}[PHASE]${NC} $message"
            ;;
    esac
}

# Function to check if command exists
check_command() {
    if ! command -v "$1" &> /dev/null; then
        print_status "ERROR" "Command '$1' not found. Please install it first."
        return 1
    fi
    return 0
}

# Function to check tool dependencies
check_dependencies() {
    print_status "INFO" "Checking tool dependencies..."
    
    local tools=("subfinder" "assetfinder" "amass" "bbot" "ffuf" "subdog" "sudomy" "dnscan" "whois" "prips" "dig" "httpx" "nuclei" "anew" "sort" "uniq" "jq")
    local missing_tools=()
    
    for tool in "${tools[@]}"; do
        if ! check_command "$tool"; then
            missing_tools+=("$tool")
        fi
    done
    
    if [ ${#missing_tools[@]} -ne 0 ]; then
        print_status "ERROR" "Missing tools: ${missing_tools[*]}"
        print_status "INFO" "Please install missing tools before running the script."
        exit 1
    fi
    
    print_status "SUCCESS" "All required tools are available."
}

# Function to create output directory structure
setup_directories() {
    local target=$1
    local base_dir="recon_${target}_${TIMESTAMP}"
    
    mkdir -p "$base_dir"/{subdomains,enumeration,intelligence,ports,screenshots,reports,wordlists,raw_output}
    mkdir -p "$base_dir"/subdomains/{subfinder,assetfinder,amass,bbot,ffuf,subdog,sudomy,dnscan}
    mkdir -p "$base_dir"/enumeration/{live_hosts,technologies,certificates}
    mkdir -p "$base_dir"/intelligence/{org_intel,asn_intel,cidr_intel,whois_data}
    
    echo "$base_dir"
}

# Function to run subfinder
run_subfinder() {
    local domain=$1
    local output_dir=$2
    
    print_status "INFO" "Running Subfinder on $domain..."
    subfinder -d "$domain" -all --recursive -o "$output_dir/subdomains/subfinder/subfinder.txt" -silent
    
    if [ -f "$output_dir/subdomains/subfinder/subfinder.txt" ]; then
        local count=$(wc -l < "$output_dir/subdomains/subfinder/subfinder.txt")
        print_status "SUCCESS" "Subfinder found $count subdomains"
    else
        print_status "WARNING" "Subfinder output file not created"
        touch "$output_dir/subdomains/subfinder/subfinder.txt"
    fi
}

# Function to run assetfinder
run_assetfinder() {
    local domain=$1
    local output_dir=$2
    
    print_status "INFO" "Running AssetFinder on $domain..."
    echo "$domain" | assetfinder -subs-only > "$output_dir/subdomains/assetfinder/assetfinder.txt" 2>/dev/null
    
    if [ -f "$output_dir/subdomains/assetfinder/assetfinder.txt" ]; then
        local count=$(wc -l < "$output_dir/subdomains/assetfinder/assetfinder.txt")
        print_status "SUCCESS" "AssetFinder found $count subdomains"
    else
        print_status "WARNING" "AssetFinder output file not created"
        touch "$output_dir/subdomains/assetfinder/assetfinder.txt"
    fi
}

# Function to run amass passive enumeration
run_amass_passive() {
    local domain=$1
    local output_dir=$2
    
    print_status "INFO" "Running Amass passive enumeration on $domain..."
    amass enum -passive -d "$domain" -o "$output_dir/subdomains/amass/amass_passive.txt" 2>/dev/null
    
    if [ -f "$output_dir/subdomains/amass/amass_passive.txt" ]; then
        local count=$(wc -l < "$output_dir/subdomains/amass/amass_passive.txt")
        print_status "SUCCESS" "Amass passive found $count subdomains"
    else
        print_status "WARNING" "Amass passive output file not created"
        touch "$output_dir/subdomains/amass/amass_passive.txt"
    fi
}

# Function to run bbot
run_bbot() {
    local domain=$1
    local output_dir=$2
    
    print_status "INFO" "Running BBOT on $domain..."
    # Run bbot with timeout and output redirection
    timeout 600 bbot -t "$domain" -p subdomain-enum cloud-enum code-enum email-enum spider web-basic paramminer dirbust-light web-screenshots --allow-deadly -o "$output_dir/subdomains/bbot/" 2>/dev/null || true
    
    # Extract subdomains from bbot output
    if [ -d "$output_dir/subdomains/bbot" ]; then
        find "$output_dir/subdomains/bbot" -name "*.txt" -exec cat {} \\; 2>/dev/null | grep -E "^[a-zA-Z0-9.-]+\\.$domain$" | sort -u > "$output_dir/subdomains/bbot/bbot_subdomains.txt" || touch "$output_dir/subdomains/bbot/bbot_subdomains.txt"
        local count=$(wc -l < "$output_dir/subdomains/bbot/bbot_subdomains.txt" 2>/dev/null || echo 0)
        print_status "SUCCESS" "BBOT found $count subdomains"
    else
        print_status "WARNING" "BBOT output directory not created"
        mkdir -p "$output_dir/subdomains/bbot"
        touch "$output_dir/subdomains/bbot/bbot_subdomains.txt"
    fi
}

# Function to run ffuf subdomain fuzzing
run_ffuf() {
    local domain=$1
    local output_dir=$2
    local wordlist="/usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt"
    
    # Use a smaller wordlist if the main one doesn't exist
    if [ ! -f "$wordlist" ]; then
        wordlist="/usr/share/wordlists/dirb/common.txt"
    fi
    
    if [ ! -f "$wordlist" ]; then
        print_status "WARNING" "No wordlist found for ffuf, skipping..."
        touch "$output_dir/subdomains/ffuf/ffuf.txt"
        return
    fi
    
    print_status "INFO" "Running ffuf subdomain fuzzing on $domain..."
    ffuf -w "$wordlist" -u "https://FUZZ.$domain" -mc 200,301,302,403 -o "$output_dir/subdomains/ffuf/ffuf.json" -of json -s 2>/dev/null || true
    
    # Extract subdomains from ffuf json output
    if [ -f "$output_dir/subdomains/ffuf/ffuf.json" ]; then
        jq -r '.results[].url' "$output_dir/subdomains/ffuf/ffuf.json" 2>/dev/null | sed 's|https\\?://||' | cut -d'/' -f1 > "$output_dir/subdomains/ffuf/ffuf.txt" || touch "$output_dir/subdomains/ffuf/ffuf.txt"
        local count=$(wc -l < "$output_dir/subdomains/ffuf/ffuf.txt")
        print_status "SUCCESS" "ffuf found $count subdomains"
    else
        print_status "WARNING" "ffuf output file not created"
        touch "$output_dir/subdomains/ffuf/ffuf.txt"
    fi
}

# Function to run subdog
run_subdog() {
    local domain=$1
    local output_dir=$2
    
    print_status "INFO" "Running subdog on $domain..."
    echo "$domain" | subdog -tools all > "$output_dir/subdomains/subdog/subdog.txt" 2>/dev/null || touch "$output_dir/subdomains/subdog/subdog.txt"
    
    if [ -f "$output_dir/subdomains/subdog/subdog.txt" ]; then
        local count=$(wc -l < "$output_dir/subdomains/subdog/subdog.txt")
        print_status "SUCCESS" "subdog found $count subdomains"
    else
        print_status "WARNING" "subdog output file not created"
        touch "$output_dir/subdomains/subdog/subdog.txt"
    fi
}

# Function to run sudomy
run_sudomy() {
    local domain=$1
    local output_dir=$2
    
    print_status "INFO" "Running sudomy on $domain..."
    timeout 300 sudomy -d "$domain" --all -o "$output_dir/subdomains/sudomy/" 2>/dev/null || true
    
    # Find and consolidate sudomy output
    find "$output_dir/subdomains/sudomy" -name "*.txt" -exec cat {} \\; 2>/dev/null | sort -u > "$output_dir/subdomains/sudomy/sudomy.txt" || touch "$output_dir/subdomains/sudomy/sudomy.txt"
    
    if [ -f "$output_dir/subdomains/sudomy/sudomy.txt" ]; then
        local count=$(wc -l < "$output_dir/subdomains/sudomy/sudomy.txt")
        print_status "SUCCESS" "sudomy found $count subdomains"
    else
        print_status "WARNING" "sudomy output file not created"
        touch "$output_dir/subdomains/sudomy/sudomy.txt"
    fi
}

# Function to run dnscan
run_dnscan() {
    local domain=$1
    local output_dir=$2
    local wordlist="/usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt"
    
    if [ ! -f "$wordlist" ]; then
        wordlist="/usr/share/wordlists/dirb/common.txt"
    fi
    
    if [ ! -f "$wordlist" ]; then
        print_status "WARNING" "No wordlist found for dnscan, skipping..."
        touch "$output_dir/subdomains/dnscan/dnscan.txt"
        return
    fi
    
    print_status "INFO" "Running dnscan on $domain..."
    dnscan -d "$domain" -w "$wordlist" -o "$output_dir/subdomains/dnscan/dnscan.txt" 2>/dev/null || touch "$output_dir/subdomains/dnscan/dnscan.txt"
    
    if [ -f "$output_dir/subdomains/dnscan/dnscan.txt" ]; then
        local count=$(wc -l < "$output_dir/subdomains/dnscan/dnscan.txt")
        print_status "SUCCESS" "dnscan found $count subdomains"
    else
        print_status "WARNING" "dnscan output file not created"
        touch "$output_dir/subdomains/dnscan/dnscan.txt"
    fi
}

# Function to aggregate and clean subdomains
aggregate_subdomains() {
    local output_dir=$1
    local domain=$2
    
    print_status "PHASE" "Aggregating and cleaning subdomain results..."
    
    # Combine all subdomain sources
    cat "$output_dir"/subdomains/*/subfinder.txt \\
        "$output_dir"/subdomains/*/assetfinder.txt \\
        "$output_dir"/subdomains/*/amass_passive.txt \\
        "$output_dir"/subdomains/*/bbot_subdomains.txt \\
        "$output_dir"/subdomains/*/ffuf.txt \\
        "$output_dir"/subdomains/*/subdog.txt \\
        "$output_dir"/subdomains/*/sudomy.txt \\
        "$output_dir"/subdomains/*/dnscan.txt 2>/dev/null | \\
        grep -E "^[a-zA-Z0-9.-]+\\.$domain$" | \\
        sort -u > "$output_dir/subdomains/all_subdomains_raw.txt"
    
    # Clean and validate subdomains
    grep -vE "(^\\.|\\.\\.|\\.\\.$|^-|-$)" "$output_dir/subdomains/all_subdomains_raw.txt" | \\
        grep -E "^[a-zA-Z0-9][a-zA-Z0-9.-]*[a-zA-Z0-9]\\.$domain$|^[a-zA-Z0-9]\\.$domain$" | \\
        sort -u > "$output_dir/subdomains/all_subdomains_clean.txt"
    
    local total_count=$(wc -l < "$output_dir/subdomains/all_subdomains_clean.txt")
    print_status "SUCCESS" "Total unique subdomains found: $total_count"
    
    # Save final list
    cp "$output_dir/subdomains/all_subdomains_clean.txt" "$output_dir/final_subdomains.txt"
}

# Function to run amass intelligence gathering
run_amass_intel() {
    local domain=$1
    local output_dir=$2
    
    print_status "PHASE" "Running Amass intelligence gathering..."
    
    # Organization intelligence
    print_status "INFO" "Gathering organization intelligence..."
    amass intel -org "$(echo $domain | cut -d'.' -f1)" -o "$output_dir/intelligence/org_intel/org_intel.txt" 2>/dev/null || touch "$output_dir/intelligence/org_intel/org_intel.txt"
    
    # If we have organization data, get ASN information
    if [ -s "$output_dir/intelligence/org_intel/org_intel.txt" ]; then
        print_status "INFO" "Gathering ASN intelligence..."
        while read -r asn_line; do
            if [[ $asn_line =~ AS[0-9]+ ]]; then
                local asn=$(echo "$asn_line" | grep -oE 'AS[0-9]+')
                amass intel -active -asn "$asn" -o "$output_dir/intelligence/asn_intel/asn_${asn}.txt" 2>/dev/null || true
            fi
        done < "$output_dir/intelligence/org_intel/org_intel.txt"
        
        # Combine all ASN results
        cat "$output_dir/intelligence/asn_intel"/*.txt > "$output_dir/intelligence/asn_intel/all_asn.txt" 2>/dev/null || touch "$output_dir/intelligence/asn_intel/all_asn.txt"
    fi
}

# Function to perform reverse DNS lookups
run_reverse_dns() {
    local output_dir=$1
    
    print_status "PHASE" "Performing reverse DNS lookups..."
    
    if [ -s "$output_dir/intelligence/asn_intel/all_asn.txt" ]; then
        print_status "INFO" "Extracting IP ranges and performing reverse DNS..."
        
        # Extract CIDR ranges and perform reverse DNS
        grep -oE "([0-9]{1,3}\\.){3}[0-9]{1,3}/[0-9]+" "$output_dir/intelligence/asn_intel/all_asn.txt" | sort -u > "$output_dir/intelligence/cidr_ranges.txt"
        
        while read -r cidr; do
            if [ ! -z "$cidr" ]; then
                print_status "INFO" "Processing CIDR range: $cidr"
                
                # Use prips to generate IP list and perform reverse DNS
                prips "$cidr" 2>/dev/null | head -100 | while read -r ip; do
                    reverse_record=$(dig -x "$ip" +short 2>/dev/null)
                    if [ ! -z "$reverse_record" ] && [ "$reverse_record" != ";" ]; then
                        echo "$ip -> $reverse_record"
                    fi
                done >> "$output_dir/intelligence/reverse_dns_results.txt" 2>/dev/null || true
            fi
        done < "$output_dir/intelligence/cidr_ranges.txt"
    fi
}

# Function to generate summary report
generate_report() {
    local output_dir=$1
    local domain=$2
    local start_time=$3
    local end_time=$4
    
    local report_file="$output_dir/reports/reconnaissance_report.txt"
    
    print_status "PHASE" "Generating reconnaissance report..."
    
    cat > "$report_file" << EOF
=============================================================================
RECONNAISSANCE REPORT
=============================================================================
Target Domain: $domain
Scan Start Time: $start_time
Scan End Time: $end_time
Duration: $((end_time - start_time)) seconds
Generated: $(date)

=============================================================================
SUBDOMAIN ENUMERATION RESULTS
=============================================================================
EOF

    # Add subdomain statistics
    echo "Tool Results:" >> "$report_file"
    for tool_dir in "$output_dir"/subdomains/*/; do
        local tool_name=$(basename "$tool_dir")
        local tool_file=$(find "$tool_dir" -name "*.txt" | head -1)
        if [ -f "$tool_file" ]; then
            local count=$(wc -l < "$tool_file")
            printf "%-15s: %d subdomains\\n" "$tool_name" "$count" >> "$report_file"
        fi
    done
    
    echo "" >> "$report_file"
    echo "Total Unique Subdomains: $(wc -l < "$output_dir/final_subdomains.txt")" >> "$report_file"
    
    # Add top 10 subdomains
    echo "" >> "$report_file"
    echo "Sample Subdomains (first 10):" >> "$report_file"
    head -10 "$output_dir/final_subdomains.txt" >> "$report_file"
    
    echo "" >> "$report_file"
    echo "==============================================================================" >> "$report_file"
    echo "FILES GENERATED:" >> "$report_file"
    echo "==============================================================================" >> "$report_file"
    echo "- final_subdomains.txt: All unique subdomains found" >> "$report_file"
    echo "- subdomains/: Individual tool outputs" >> "$report_file"
    echo "- intelligence/: Organization and ASN intelligence" >> "$report_file"
    echo "- reports/: This report and other analysis files" >> "$report_file"
    
    print_status "SUCCESS" "Report generated: $report_file"
}

# Function to run parallel subdomain enumeration
run_parallel_enumeration() {
    local domain=$1
    local output_dir=$2
    
    print_status "PHASE" "Starting parallel subdomain enumeration..."
    
    # Create a job control function
    run_job() {
        local func_name=$1
        local domain=$2
        local output_dir=$3
        
        # Run the function and capture any errors
        $func_name "$domain" "$output_dir" 2>&1
    }
    
    # Array of functions to run in parallel
    local enum_functions=("run_subfinder" "run_assetfinder" "run_amass_passive")
    
    # Start parallel jobs
    local pids=()
    for func in "${enum_functions[@]}"; do
        run_job "$func" "$domain" "$output_dir" &
        pids+=($!)
        
        # Limit parallel jobs
        if [ ${#pids[@]} -ge $MAX_PARALLEL_JOBS ]; then
            wait "${pids[0]}"
            pids=("${pids[@]:1}")
        fi
    done
    
    # Wait for remaining jobs
    for pid in "${pids[@]}"; do
        wait "$pid"
    done
    
    # Run sequential jobs (these tools don't play well with parallel execution)
    run_bbot "$domain" "$output_dir"
    run_ffuf "$domain" "$output_dir"
    run_subdog "$domain" "$output_dir"
    run_sudomy "$domain" "$output_dir"
    run_dnscan "$domain" "$output_dir"
}

# Main function
main() {
    local domain=$1
    
    # Validate input
    if [ -z "$domain" ]; then
        echo "Usage: $0 <domain>"
        echo "Example: $0 example.com"
        exit 1
    fi
    
    # Remove protocol and path if provided
    domain=$(echo "$domain" | sed 's|^https\\?://||' | cut -d'/' -f1)
    
    print_banner
    
    local start_time=$(date +%s)
    
    # Check dependencies
    check_dependencies
    
    # Setup directories
    local output_dir=$(setup_directories "$domain")
    print_status "INFO" "Output directory: $output_dir"
    
    # Run parallel enumeration
    run_parallel_enumeration "$domain" "$output_dir"
    
    # Aggregate results
    aggregate_subdomains "$output_dir" "$domain"
    
    # Run intelligence gathering
    run_amass_intel "$domain" "$output_dir"
    
    # Run reverse DNS lookups
    run_reverse_dns "$output_dir"
    
    local end_time=$(date +%s)
    
    # Generate report
    generate_report "$output_dir" "$domain" "$start_time" "$end_time"
    
    print_status "SUCCESS" "Reconnaissance completed!"
    print_status "INFO" "Results saved in: $output_dir"
    print_status "INFO" "Final subdomain list: $output_dir/final_subdomains.txt"
    print_status "INFO" "Full report: $output_dir/reports/reconnaissance_report.txt"
}

# Error handling
set -eE
trap 'print_status "ERROR" "Script interrupted or failed at line $LINENO"' ERR

# Run main function with all arguments
main "$@"
'''

# Save the script to a file
with open("advanced_recon.sh", "w") as f:
    f.write(script_content)

print("Advanced reconnaissance script created: advanced_recon.sh")
print("\nScript features:")
print("✓ Parallel execution of reconnaissance tools")
print("✓ Comprehensive error handling and logging")
print("✓ Organized output directory structure")
print("✓ Automated aggregation and deduplication")
print("✓ Intelligence gathering with Amass")
print("✓ Reverse DNS lookups")
print("✓ Detailed reporting")
print("✓ Color-coded status messages")
print("✓ Dependency checking")