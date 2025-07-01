# client/agent.py
import json, os
from typing import Dict, List
from contextlib import AsyncExitStack

from openai import OpenAI
from client.client import MCPClient
from utils.utils import formatted_mcp_servers

SERVER_PATHS = ["servers/WeatherServer.py", "servers/MathServer.py"]


class MCPAgent:
    """
    封装多个 MCPClient，并负责与 LLM 对话。
    用法:
        async with MCPAgent() as agent:
            reply = await agent.process_query("天气怎么样?")
    """

    def __init__(self):
        self.llm = OpenAI(
            api_key=os.getenv("API_KEY"),
            base_url=os.getenv("BASE_URL"),
        )
        self.exit_stack: AsyncExitStack | None = None
        self.mcp_clients: Dict[str, MCPClient] = {}
        self.history: List[dict] = []

    # ---------- async context manager ----------
    async def __aenter__(self) -> "MCPAgent":
        self.exit_stack = AsyncExitStack()
        await self.exit_stack.__aenter__()

        # 启动所有 server
        server_desc = []
        for path in SERVER_PATHS:
            client = MCPClient(path)
            client = await self.exit_stack.enter_async_context(client)  # type: ignore
            self.mcp_clients[client.server_description["server_name"]] = client
            server_desc.append(client.server_description)

        # 构造 system prompt
        with open("prompts/chat_sys_prompt.txt") as f:
            system_prompt = f.read()
        system_prompt = system_prompt.format(
            Available_Servers=formatted_mcp_servers(server_desc)
        )

        self.history = [{"role": "system", "content": system_prompt}]
        return self

    async def __aexit__(self, exc_type, exc, tb):
        # 统一关闭所有子 context
        await self.exit_stack.__aexit__(exc_type, exc, tb)

    # ---------- chat ----------
    async def process_query(self, query: str) -> str:
        self.history.append({"role": "user", "content": query})

        response = self.llm.chat.completions.create(
            model=os.getenv("MODEL"), messages=self.history
        )
        reply = response.choices[0].message.content.strip()

        # 尝试解析为工具调用指令
        try:
            cmd = json.loads(reply)
            if {"server", "tool", "tool_params"} <= cmd.keys():
                tool_result = await self.mcp_clients[cmd["server"]].call_tool(
                    cmd["tool"], cmd["tool_params"]
                )

                # 把调用过程塞回对话历史
                self.history.extend(
                    [
                        {"role": "assistant", "content": reply},
                        {"role": "assistant", "content": tool_result},
                    ]
                )

                # 再让 LLM 生成最终回复
                final_resp = self.llm.chat.completions.create(
                    model=os.getenv("MODEL"), messages=self.history
                )
                final_reply = final_resp.choices[0].message.content.strip()
                self.history.append({"role": "assistant", "content": final_reply})
                return final_reply
        except json.JSONDecodeError:
            pass  # 普通文本回复

        self.history.append({"role": "assistant", "content": reply})
        return reply