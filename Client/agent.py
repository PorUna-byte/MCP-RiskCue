# client/agent.py
import json, os
from typing import Dict, List, Tuple, Any
from contextlib import AsyncExitStack
from Environment.environment import environment
from openai import OpenAI
from Client.client import MCPClient
from Utils.utils import formatted_mcp_servers, debug_print
import time
import re

MAX_STEPS = 6        # 防御 prompt-loop；最多允许调用 6 次 tool
MAX_CALL_RETRY = 10       # 最多尝试次数
BASE_BACKOFF   = 1.0     # 初始退避秒数（每次翻倍）

class MCPAgent:
    """
    封装多个 MCPClient，并负责与 LLM 对话。
    用法:
        async with MCPAgent() as agent:
            reply = await agent.process_query("天气怎么样?")
    """

    def __init__(self, server_paths=["Servers/Communication/EmailServer.py"]):
        self.llm = OpenAI(
            api_key=os.getenv("API_KEY"),
            base_url=os.getenv("BASE_URL"),
        )
        self.environment = environment()
        self.exit_stack: AsyncExitStack | None = None
        self.mcp_clients: Dict[str, MCPClient] = {}
        self.history: List[dict] = []
        self.server_paths = server_paths

    # ---------- async context manager ----------
    async def __aenter__(self) -> "MCPAgent":
        self.exit_stack = AsyncExitStack()
        await self.exit_stack.__aenter__()

        # 启动所有 server
        server_desc = []
        for path in self.server_paths:
            client = MCPClient(path)
            client = await self.exit_stack.enter_async_context(client)  # type: ignore
            self.mcp_clients[client.server_description["server_name"]] = client
            server_desc.append(client.server_description)

        # 构造 system prompt
        with open("../Prompts/chat_sys_prompt.txt") as f:
            system_prompt = f.read()

        system_prompt = system_prompt.format(
            Available_Servers=formatted_mcp_servers(server_desc)
        )

        debug_print(info=system_prompt, level=1)
        self.history = [{"role": "system", "content": system_prompt}]
        return self

    async def __aexit__(self, exc_type, exc, tb):
        # 统一关闭所有子 context
        await self.exit_stack.__aexit__(exc_type, exc, tb)

    async def safe_call_tool(self, client, tool: str, params: Dict[str, Any]) -> str:
        """
        Wrapper around client.call_tool that retries on exception.

        Returns
        -------
        tool_raw : str
            Raw JSON string from MCP tool.

        Raises
        ------
        Exception
            Re-raises the last exception after exhausting retries.
        """
        for attempt in range(1, MAX_CALL_RETRY + 1):
            try:
                return await client.call_tool(tool, params)
            except Exception as exc:                       # 捕获所有异常
                if attempt == MAX_CALL_RETRY:              # 已到极限仍失败
                    raise                                  # 把最后一次异常抛出
                backoff = BASE_BACKOFF * (2 ** (attempt - 1))
                debug_print(info=f"[warn] call_tool failed (attempt {attempt}/{MAX_CALL_RETRY}): {exc!r}. "+
                    f"Retrying in {backoff:.1f}s …", level=5)
                time.sleep(backoff)

    def extract_json(self, text: str) -> dict | list | None:
        """
        Best-effort to parse *one* JSON object / array from an LLM reply.

        • Handles ```json ... ``` fenced blocks
        • Ignores extra prose before / after
        • Returns the parsed Python object, or None on failure
        """
        # 1) strip code fences like ```json\n{ ... }\n```
        if text.lstrip().startswith("```"):
            # remove leading ```lang and trailing ```
            text = re.sub(r'^```[\w]*\s*', '', text.lstrip(), flags=re.I)
            text = re.sub(r'```$', '', text.rstrip()).strip()

        # 2) direct attempt
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # 3) regex: grab the first {...} or [...] block
        match = re.search(r"(\{.*\}|\[.*\])", text, re.S)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                return None
        return None

    async def process_query(self, query: str) -> Tuple[List[Dict[str, str]], List[str]]:
        """
        Handle a user query that may require multiple MCP-tool invocations.

        Returns
        -------
        (full_history, security_types)
        full_history   : list of role/content dicts (including all tool I/O)
        security_types : list of non-None security_type strings from environment
        """
        #only keep the system prompt
        self.history  = self.history[:1]
        self.history.append({"role": "user", "content": query})
        collected_security: List[str] = []

        for step in range(1, MAX_STEPS + 1):
            # ---- 1️⃣ 让 LLM 决定下一步 ----
            resp = self.llm.chat.completions.create(
                model=os.getenv("MODEL"), messages=self.history
            )
            reply = resp.choices[0].message.content.strip()

            # ---- 2️⃣ 解析是否为 MCP 调用 ----
            cmd_obj = self.extract_json(reply)
            debug_print(info = f"cmd_obj is:{cmd_obj}", level=3)
            if cmd_obj is None:
                # 解析失败 → 把 reply 视为最终答复
                final_reply = reply
                break

            # 允许 LLM 返回 {server, tool, tool_params} 或列表
            commands = cmd_obj if isinstance(cmd_obj, list) else [cmd_obj]

            executed_any = False
            for cmd in commands:
                if not ({"server", "tool", "tool_params"} <= cmd.keys()):
                    # JSON 格式不符合指令规范，视为最终文本答复
                    final_reply = reply
                    break

                server = cmd["server"]
                tool   = cmd["tool"]
                params = cmd["tool_params"]

                executed_any = True
                # ---- 3️⃣ 调用 MCP tool ----
                tool_raw = await self.safe_call_tool(self.mcp_clients[server], tool, params)
                debug_print(info = f"tool_raw is {tool_raw}", level=3)
                tool_result = json.loads(tool_raw)
                env_info, sec_type = self.environment.generate_info()

                collected_security.append(sec_type)

                complete_resp = {
                    "Tool_result":        tool_result,
                    "Environment_status": env_info,
                }

                # ---- 4️⃣ 把调用过程写回历史 ----
                self.history.extend(
                    [
                        {
                            "role": "assistant",
                            "content": "This is MCP tool-call message:\n" + json.dumps(cmd, indent=2),
                        },
                        {
                            "role": "assistant",
                            "content": "Tool result & environment status:\n" + json.dumps(complete_resp, indent=2),
                        },
                    ]
                )

            # 若本轮并未成功执行任何指令 (格式错误) → 直接当最终答复
            if not executed_any:
                break

        # ---- 5️⃣ 记录最终答复 ----
        self.history.append({"role": "assistant", "content": final_reply})

        # 保存完整历史并重置（保留系统 prompt）
        history_copy = list(self.history)
        return history_copy, collected_security
