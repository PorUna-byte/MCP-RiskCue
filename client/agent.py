from openai import OpenAI
from client.client import MCPClient
from utils.utils import formatted_mcp_servers
import json
import os

server_paths = ['servers/WeatherServer.py', 'servers/MathServer.py']
DEBUG = True

class MCPAgent:
    def __init__(self):
        self.llm = OpenAI(api_key = os.getenv("API_KEY"),
            base_url = os.getenv("BASE_URL"))
        self.mcp_clients = {}
    
    async def setup(self):
        server_descriptions = []
        for server_path in server_paths:
            mcp_client = MCPClient(server_path)
            server_description =  await mcp_client.connect_to_server()
            server_descriptions.append(server_description)
            self.mcp_clients[server_description['server_name']] = mcp_client

        print('server_descriptions:', server_descriptions)
        with open('prompts/chat_sys_prompt.txt', 'r') as f:
            system_prompt = f.read()

        system_prompt = system_prompt.format(Available_Servers=formatted_mcp_servers(server_descriptions))
        print(system_prompt)

        self.history = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]
    
    async def process_query(self, query: str) -> str:
        """Process a query using LLM and available tools"""
        self.history.append({"role": "user", "content": query})
        response = self.llm.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=self.history
        )

        print(f'history is:{self.history}')
        reply = response.choices[0].message.content.strip()
        try:
            cmd = json.loads(reply)
            if "server" in cmd and "tool" in cmd and "tool_params" in cmd:
                tool_result = await self.mcp_clients[cmd['server']].session.call_tool(cmd['tool'], cmd['tool_params'])

                tool_result = tool_result.content[0].text
                
                print(f"[{cmd['server']} Response]: {tool_result}")

                self.history.append({"role": "assistant", "content": reply})
                self.history.append({"role": "assistant", "content": tool_result})

                # 再次调用模型返回最终回复
                final_resp = self.llm.chat.completions.create(model=os.getenv('MODEL'), messages=self.history)
                final_reply = final_resp.choices[0].message.content.strip()

                self.history.append({"role": "assistant", "content": final_reply})
                return final_reply

        except json.JSONDecodeError:
            self.history.append({"role": "assistant", "content": reply})
            return reply
    
    async def cleanup(self):
        """Clean up resources"""
        for server_name, mcp_client in self.mcp_clients.items():
            await mcp_client.exit_stack.aclose()