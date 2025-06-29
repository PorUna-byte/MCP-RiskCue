def formatted_mcp_servers(server_descriptions):
    prompt = ""
    
    for server in server_descriptions:
        prompt += f"1. {server['server_name']} Service:\n"
        
        for tool in server['tools']:
            # Get required inputs with their types
            required_inputs = [
                f"'{param}' ({details['type']})" 
                for param, details in tool['input_schema']['properties'].items()
            ]
            
            prompt += f"   - Tool: {tool['name']}\n"
            prompt += f"     Description: {tool['description'] or 'No description provided'}\n"
            prompt += f"     Required Parameters: {', '.join(required_inputs)}\n"
    
    prompt += """Instructions:
- Always verify you have all required parameters before calling a tool
- Return complete information in the response
- Ask for clarification if any parameters are unclear\n"""
    
    return prompt

def formatted_tool_result():
    pass
