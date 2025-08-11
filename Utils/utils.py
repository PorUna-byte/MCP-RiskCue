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

