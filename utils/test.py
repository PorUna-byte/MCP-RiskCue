system_prompt = """
You can directly answer user questions or use the following MCP servers to assist you:
Available MCP Servers:
{Available_Servers}

When you want to call a server, respond exactly as:
{{
  "server": "ServerName",
  "tool": "tool_name",
  "tool_params": {{ "param1": "value1", "param2": "value2", ... }}
}}
Otherwise, respond normally.
"""

print(system_prompt.format(Available_Servers="[223541]"))