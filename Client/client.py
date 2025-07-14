# client/client.py
from __future__ import annotations
from typing import Optional, Dict, Any
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClient:
    """
    单个 MCP server 的生命周期封装：
    async with MCPClient(path) as client:  # 自动连接/关闭
        await client.call_tool(...)
    """

    def __init__(self, server_script_path: str):
        self.server_script_path = server_script_path
        self.exit_stack: Optional[AsyncExitStack] = None
        self.session: Optional[ClientSession] = None
        self.server_description: Dict[str, Any] = {}

    # ---------- async context manager ----------
    async def __aenter__(self) -> "MCPClient":
        self.exit_stack = AsyncExitStack()
        await self.exit_stack.__aenter__()
        await self._connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        # 统一在同一 task 中退出，彻底避免 cancel-scope mismatch
        await self.exit_stack.__aexit__(exc_type, exc, tb)

    # ---------- public helpers ----------
    async def call_tool(self, tool_name: str, tool_params: Dict[str, Any]) -> str:
        """调用 server 上的工具并返回纯文本结果"""
        result = await self.session.call_tool(tool_name, tool_params)
        return result.content[0].text  # MCP SDK 约定格式

    # ---------- internal ----------
    async def _connect(self):
        is_python = self.server_script_path.endswith(".py")
        is_js = self.server_script_path.endswith(".js")
        if not (is_python or is_js):
            raise ValueError("Server script must be .py or .js")

        server_name = self.server_script_path.split("/")[-1][:-3]

        params = StdioServerParameters(
            command="python" if is_python else "node",
            args=[self.server_script_path],
            env=None,
        )

        # 1) 启动子进程并拿到 (read, write) stream
        read_stream, write_stream = await self.exit_stack.enter_async_context(
            stdio_client(params)
        )

        # 2) 创建并初始化 session
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(read_stream, write_stream)
        )
        await self.session.initialize()

        # 3) 保存 server 描述，供上层生成系统提示
        resp = await self.session.list_tools()
        self.server_description = {
            "server_name": server_name,
            "tools": [
                {
                    "name": t.name,
                    "description": t.description,
                    "input_schema": t.inputSchema,
                }
                for t in resp.tools
            ],
        }
