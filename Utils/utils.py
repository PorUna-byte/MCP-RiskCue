import textwrap
LEVEL = 5

def formatted_mcp_servers(server_descriptions) -> str:
    """Return a nicely-aligned, human-readable list of MCP servers / tools."""
    lines = []

    for idx, server in enumerate(server_descriptions, start=1):
        lines.append(f"{idx}. {server['server_name']} Service:")
        lines.append("")  # blank line after server header

        for tool in server["tools"]:
            # ---------- header line ----------
            lines.append(f"   - Tool: {tool['name']}")

            # ---------- description block ----------
            desc = tool.get("description") or "No description provided."
            desc_block = textwrap.indent(textwrap.dedent(desc).strip(), "     ")
            lines.append("     Description:")
            lines.append(desc_block)
            lines.append("")  # space between Description and “Parameters”

            # ---------- required parameters ----------
            required = [
                f"'{p}' ({meta['type']})"
                for p, meta in tool["input_schema"]["properties"].items()
            ]
            rp_line = ", ".join(required) if required else "None"
            lines.append(f"     Required Parameters: {rp_line}")
            lines.append("")  # blank line between tools

        # extra blank line between servers
        lines.append("")

    prompt = "\n".join(lines).rstrip()
    return prompt

def debug_print(info, level):
    if level>=LEVEL:
        print(info)

def is_valid_response(resp_list):
    EXPECTED_ROLES = ["system", "user", "assistant", "assistant", "assistant","assistant"]
    """Return True if resp_list matches the required structure."""
    if not isinstance(resp_list, list) or len(resp_list) < 5:
        return False
    for elem, role in zip(resp_list[:5], EXPECTED_ROLES):
        if not isinstance(elem, dict) or elem.get("role") != role:
            return False
    return True

def is_valid_security(sec_list):
    if not isinstance(sec_list, list):
        return False
    
    if len(sec_list)==0:
        return False
    
    if sec_list[0] == None:
        return False
    
    for sec in sec_list:
        if sec not in ["Sensitive Data Exfiltration", "Covert Channel Attack", "Malicious Code Execution",
        "Privilege Escalation", "Persistence via Backdoor Implantation", "Cache or Local State Pollution",
        "Delayed or Timed Trigger Attacks", "Denial-of-Service", "Log Explosion Attacks", "Safe"]:
            return False
    
    return True