# client/agent.py
import json, os
from typing import Dict, List, Tuple, Any
from contextlib import AsyncExitStack
from Environment.environment import environment
from openai import OpenAI
from Client.client import MCPClient
from Client.model_manager import get_model_manager
from Client.config import ModelConfig
from Utils.utils import formatted_mcp_servers, debug_print
import time
import re
from pathlib import Path

MAX_STEPS = 6        # 防御 prompt-loop；最多允许调用 6 次 tool
MAX_CALL_RETRY = 3       # 最多尝试次数
BASE_BACKOFF   = 1.0     # 初始退避秒数（每次翻倍）
Project_Root = Path(__file__).resolve().parent.parent

class MCPAgent:
    """
    封装多个 MCPClient，并负责与 LLM 对话。
    用法:
        async with MCPAgent() as agent:
            reply = await agent.process_query("天气怎么样?")
    """

    def __init__(self, server_paths=["Servers/Communication/EmailServer.py"], sys_prompt_path="sys_prompt_env.txt", model_manager=None):
        # 检查是否使用本地模型
        self.use_local_model = ModelConfig.is_local_model()
        
        if self.use_local_model:
            # 使用本地模型
            self.model_manager = model_manager or get_model_manager()
            self.llm = None
        else:
            # 使用API模型
            api_key, base_url, model = ModelConfig.get_api_config()
            self.llm = OpenAI(
                api_key=api_key,
                base_url=base_url,
            )
            self.model_manager = None
            
        self.sys_prompt_path=sys_prompt_path
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
        with open(Project_Root / "Prompts" / self.sys_prompt_path) as f:
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
                    f"Retrying in {backoff:.1f}s …", level=4)
                time.sleep(backoff)

    def extract_toll_call_json(self, text: str) -> dict | None:
        """
        Best-effort to parse *one* JSON object from an LLM reply.

        • Handles ```json ... ``` fenced blocks
        • Handles <tool_call> tags with MCP tool-call message
        • Ignores extra prose before / after
        • If server field is "ServerName", continues matching until finding valuable answer
        • Returns the parsed Python dict, or None on failure
        """
        if not text or not isinstance(text, str):
            return None
        
        # 忽略大小写和空格，支持各种格式变化，包括嵌套字典
        dict_pattern = r'\{\s*["\']?server["\']?\s*:\s*["\']?([^"\',}]+)["\']?\s*,\s*["\']?tool["\']?\s*:\s*["\']?([^"\',}]+)["\']?\s*,\s*["\']?tool_params["\']?\s*:\s*(\{.*?\})\s*\}'
        
        # 使用findall找到所有匹配的JSON对象
        all_matches = re.findall(dict_pattern, text, re.IGNORECASE | re.DOTALL)
        
        for match in all_matches:
            try:
                server = match[0].strip().strip('"\'')
                tool = match[1].strip().strip('"\'')
                tool_params_str = match[2].strip()
                
                # 如果server字段是"ServerName"，说明这是思考片段，继续匹配下一个
                if server.lower() == "servername":
                    continue
                
                # 尝试解析tool_params，支持嵌套字典
                tool_params = {}
                try:
                    tool_params = json.loads(tool_params_str)
                except json.JSONDecodeError:
                    # 如果JSON解析失败，尝试手动解析
                    # 首先尝试匹配简单的键值对（字符串值）
                    simple_params = {}
                    simple_pattern = r'["\']?([^"\',\s]+)["\']?\s*:\s*["\']?([^"\',}]+)["\']?'
                    simple_matches = re.findall(simple_pattern, tool_params_str)
                    for k, v in simple_matches:
                        simple_params[k.strip().strip('"\'')] = v.strip().strip('"\'')
                    
                    # 然后尝试匹配嵌套字典
                    nested_pattern = r'["\']?([^"\',\s]+)["\']?\s*:\s*(\{[^}]*\})'
                    nested_matches = re.findall(nested_pattern, tool_params_str)
                    for k, v in nested_matches:
                        try:
                            nested_dict = json.loads(v)
                            simple_params[k.strip().strip('"\'')] = nested_dict
                        except json.JSONDecodeError:
                            # 如果嵌套字典解析失败，作为字符串处理
                            simple_params[k.strip().strip('"\'')] = v.strip()
                    
                    tool_params = simple_params
                
                result = {
                    "server": server,
                    "tool": tool,
                    "tool_params": tool_params
                }
                return result
            except Exception:
                continue
                    
        return None

    async def _get_llm_response(self, messages: List[Dict[str, str]]) -> str:
        """获取LLM回复，支持本地模型和API模型"""
        if self.use_local_model:
            # 使用本地模型
            return await self.model_manager.generate_response(messages)
        else:
            # 使用API模型
            api_key, base_url, model = ModelConfig.get_api_config()
            resp = self.llm.chat.completions.create(
                model=model, messages=messages
            )
            return resp.choices[0].message.content.strip()

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
            reply = await self._get_llm_response(self.history)
            debug_print(info = f"initial reply is:{reply}", level=3)
            # ---- 2️⃣ 解析是否为 MCP 调用 ----
            cmd_obj = self.extract_toll_call_json(reply)
            debug_print(info = f"cmd_obj is:{cmd_obj}", level=3)
            if cmd_obj is None:
                # 解析失败 → 把 reply 视为最终答复
                final_reply = reply
                break

            # LLM只返回单个对象 {server, tool, tool_params}
            if not ({"server", "tool", "tool_params"} <= cmd_obj.keys()):
                # JSON 格式不符合指令规范，视为最终文本答复
                final_reply = reply
                break

            server = cmd_obj["server"]
            tool   = cmd_obj["tool"]
            params = cmd_obj["tool_params"]

            # 处理server字段，去除可能的后缀如'service'
            server = re.sub(r'service$', '', server, flags=re.I).strip()
            
            # 检查server是否存在于mcp_clients中
            if server not in self.mcp_clients:
                debug_print(info=f"Server '{server}' not found in available clients", level=3)
                final_reply = reply
                break

            # ---- 3️⃣ 调用 MCP tool ----
            tool_raw = await self.safe_call_tool(self.mcp_clients[server], tool, params)
            debug_print(info = f"tool_raw is {tool_raw}", level=3)
            tool_result = json.loads(tool_raw)
            env_info, sec_type = self.environment.generate_info()

            collected_security.append(sec_type)
            tool_result_dict = {}

            if "env" in self.sys_prompt_path:
                complete_resp = {
                    "Tool_result": tool_result,
                    "Environment_status": env_info,
                }
                tool_result_dict = {
                    "role": "user",
                    "content": "Tool result & environment status:\n" + json.dumps(complete_resp, indent=2),
                }

            elif "prin" in self.sys_prompt_path:
                complete_resp = {
                    "Tool_result": tool_result
                }
                tool_result_dict =  {
                    "role": "user",
                    "content": "Tool result:\n" + json.dumps(complete_resp, indent=2),
                }

            else:
                raise Exception(f"Unsupported system prompt path: {self.sys_prompt_path}")

            # ---- 4️⃣ 把调用过程写回历史 ----
            self.history.extend(
                [
                    {
                        "role": "assistant",
                        "content": reply,
                    },
                    tool_result_dict
                ]
            )

        # ---- 5️⃣ 记录最终答复 ----
        self.history.append({"role": "assistant", "content": final_reply})

        # 保存完整历史并重置（保留系统 prompt）
        history_copy = list(self.history)
        return history_copy, collected_security
