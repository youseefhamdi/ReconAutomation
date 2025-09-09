# Create a comparison table of the tools and their features

import pandas as pd

tools_comparison = {
    'Tool': ['Subfinder', 'AssetFinder', 'Amass', 'BBOT', 'FFUF', 'Subdog', 'Sudomy', 'DNScan'],
    'Type': ['Passive', 'Passive', 'Passive/Active', 'Active', 'Active', 'Passive', 'Passive/Active', 'Active'],
    'Speed': ['Fast', 'Very Fast', 'Medium', 'Slow', 'Medium', 'Fast', 'Medium', 'Fast'],
    'Sources': ['55+', '10+', '100+', '50+', 'Brute Force', '20+', '30+', 'Brute Force'],
    'API_Keys': ['Optional', 'No', 'Optional', 'Optional', 'No', 'No', 'Optional', 'No'],
    'Output_Quality': ['High', 'Medium', 'Very High', 'High', 'Medium', 'Medium', 'High', 'Medium'],
    'False_Positives': ['Low', 'Medium', 'Very Low', 'Low', 'High', 'Medium', 'Low', 'High'],
    'Memory_Usage': ['Low', 'Very Low', 'Medium', 'High', 'Low', 'Low', 'Medium', 'Low']
}

df = pd.DataFrame(tools_comparison)

# Save as CSV
df.to_csv('reconnaissance_tools_comparison.csv', index=False)

print("Reconnaissance Tools Comparison")
print("=" * 50)
print(df.to_string(index=False))

# Create a features overview
features_overview = '''
RECONNAISSANCE SCRIPT FEATURES OVERVIEW
======================================

ADVANCED SCRIPT (advanced_recon.sh):
✓ Parallel execution for faster results
✓ Comprehensive error handling with trap
✓ Color-coded status messages
✓ Dependency checking before execution
✓ Organized directory structure
✓ Automatic aggregation and deduplication
✓ Intelligence gathering with multiple phases
✓ Reverse DNS lookups with CIDR processing
✓ Detailed reporting with statistics
✓ Progress tracking and timing
✓ Job control for resource management
✓ Robust cleanup on script interruption

SIMPLE SCRIPT (simple_recon.sh):
✓ Sequential execution (follows your exact workflow)
✓ Basic error handling
✓ Clean output organization
✓ Summary reporting
✓ Easy to understand and modify
✓ Direct tool-to-tool pipeline
✓ Timeout handling for hanging processes
✓ Automatic wordlist detection
✓ Intelligence gathering automation
✓ Results aggregation

COMMON FEATURES:
✓ Automated subdomain enumeration
✓ Multi-tool integration
✓ Output deduplication
✓ Intelligence gathering
✓ Reverse DNS analysis
✓ Organized file structure
✓ Progress notifications
✓ Error resilience
'''

print(features_overview)

# Create usage examples
usage_examples = '''
USAGE EXAMPLES
=============

Basic Usage:
./simple_recon.sh example.com
./advanced_recon.sh example.com

The scripts will automatically:
1. Create timestamped output directories
2. Run all reconnaissance tools
3. Aggregate and deduplicate results
4. Perform intelligence gathering
5. Generate summary reports

Output Files Generated:
- final/all_subdomains.txt: All unique subdomains found
- intelligence/org_intel.txt: Organization intelligence
- intelligence/reverse_dns.txt: Reverse DNS results
- summary.txt: Complete reconnaissance summary
- Individual tool outputs in subdomains/ directory

Expected Runtime:
- Small domain (< 100 subdomains): 5-10 minutes
- Medium domain (100-1000 subdomains): 10-30 minutes  
- Large domain (1000+ subdomains): 30+ minutes

Resource Requirements:
- RAM: 2-4 GB recommended
- Disk: 100-500 MB per domain
- Network: Stable internet connection
- CPU: Multi-core recommended for parallel execution
'''

print(usage_examples)