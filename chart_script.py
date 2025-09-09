import plotly.graph_objects as go
import json

# Data for the reconnaissance workflow
data = {
    "workflow_steps": [
        {"phase": "Input", "step": "Domain Target", "tools": []}, 
        {"phase": "Subdomain Enumeration", "step": "Parallel Tool Execution", "tools": ["Subfinder", "AssetFinder", "Amass Passive", "BBOT", "FFUF", "Subdog", "Sudomy", "DNScan"]}, 
        {"phase": "Processing", "step": "Aggregation & Deduplication", "tools": ["Sort", "Uniq", "Grep"]}, 
        {"phase": "Intelligence", "step": "Amass Intel Gathering", "tools": ["Org Intel", "ASN Intel", "CIDR Intel"]}, 
        {"phase": "Network Analysis", "step": "Reverse DNS Lookups", "tools": ["Whois", "Prips", "Dig"]}, 
        {"phase": "Output", "step": "Report Generation", "tools": ["Summary Report", "Subdomain Lists", "Intelligence Data"]}
    ]
}

# Create nodes and links for Sankey diagram
nodes = []
links = []
node_colors = ['#1FB8CD', '#DB4545', '#2E8B57', '#5D878F', '#D2BA4C', '#B4413C']

# Add main phase nodes
phases = ["Input", "Subdomain Enum", "Processing", "Intelligence", "Network Analysis", "Output"]
for i, phase in enumerate(phases):
    nodes.append(phase)

# Add tool nodes for each phase
tool_nodes = []
for step in data["workflow_steps"]:
    if step["tools"]:
        for tool in step["tools"]:
            # Truncate tool names to 15 characters
            tool_short = tool[:15] if len(tool) > 15 else tool
            tool_nodes.append(tool_short)
            nodes.append(tool_short)

# Create links
node_indices = {node: i for i, node in enumerate(nodes)}

# Main flow between phases
main_flow_values = [1, 8, 1, 3, 3, 3]  # Based on number of tools in each phase
for i in range(len(phases) - 1):
    if i == 0:  # Input to Subdomain Enum
        links.append({
            'source': node_indices[phases[i]], 
            'target': node_indices[phases[i+1]], 
            'value': 1
        })
    else:
        links.append({
            'source': node_indices[phases[i]], 
            'target': node_indices[phases[i+1]], 
            'value': main_flow_values[i]
        })

# Links from phases to their tools
current_phase_idx = 0
for step in data["workflow_steps"]:
    phase_name = phases[current_phase_idx] if current_phase_idx < len(phases) else step["phase"]
    
    if step["tools"]:
        for tool in step["tools"]:
            tool_short = tool[:15] if len(tool) > 15 else tool
            if phase_name in node_indices and tool_short in node_indices:
                links.append({
                    'source': node_indices[phase_name],
                    'target': node_indices[tool_short],
                    'value': 1
                })
    current_phase_idx += 1

# Create the Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=nodes,
        color=[node_colors[i % len(node_colors)] for i in range(len(nodes))]
    ),
    link=dict(
        source=[link['source'] for link in links],
        target=[link['target'] for link in links],
        value=[link['value'] for link in links],
        color='rgba(31, 184, 205, 0.3)'  # Semi-transparent cyan
    )
)])

fig.update_layout(
    title="Recon Automation Workflow",
    font_size=12
)

fig.write_image("recon_workflow.png")