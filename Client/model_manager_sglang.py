import os
import sys
import socket
import time
import subprocess
import threading
import queue
from typing import List, Dict, Optional

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# 仅客户端依赖；服务端我们用 subprocess 启动 CLI
try:
    from sglang import RuntimeEndpoint
    SGLANG_AVAILABLE = True
    print("[Info] SGLang client available (RuntimeEndpoint).")
except Exception as _e:
    SGLANG_AVAILABLE = False
    print(f"[Warn] SGLang client not available ({_e}). Falling back to transformers.")

from Client.config import ModelConfig

def selective_decode(tokenizer, ids,
                     keep_special_tokens=["<|im_start|>", "<|im_end|>", "<|start_header_id|>", "<|end_header_id|>", "<|eot_id|>", "<start_of_turn>", "<end_of_turn>", "<|begin_of_text|>"]):
    keep_ids = {tokenizer.convert_tokens_to_ids(t) for t in keep_special_tokens}
    bos_id = tokenizer.bos_token_id
    eos_id = tokenizer.eos_token_id
    all_special_ids = set(tokenizer.all_special_ids)
    filtered = []
    for i in ids:
        if bos_id is not None and i == bos_id and i not in keep_ids:
            continue
        if eos_id is not None and i == eos_id and i not in keep_ids:
            continue
        if i in all_special_ids and i not in keep_ids:
            continue
        filtered.append(i)
    return tokenizer.decode(filtered, skip_special_tokens=False, clean_up_tokenization_spaces=False)

# ---------- SGLang server process manager (code-only launch) ----------
def _is_port_open(host: str, port: int) -> bool:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.2)
    try:
        s.connect((host, port))
        s.close()
        return True
    except Exception:
        return False
    finally:
        try:
            s.close()
        except Exception:
            pass

class SGLangServerProc:
    """Launch `python -m sglang.launch_server` as a child process from code."""
    def __init__(self,
                 model_path: str,
                 tokenizer_path: Optional[str] = None,
                 host: str = "127.0.0.1",
                 port: int = 30000,
                 tensor_parallel_size: Optional[int] = None,
                 dtype: str = "float16",
                 max_num_seqs: int = 512,
                 max_num_batched_tokens: int = 8192,
                 context_length: Optional[int] = None,
                 extra_args: Optional[list] = None,
                 env: Optional[dict] = None):
        self.model_path = model_path
        self.tokenizer_path = tokenizer_path or model_path
        self.host = host
        self.port = port
        self.tp = tensor_parallel_size or max(1, torch.cuda.device_count() if torch.cuda.is_available() else 1)
        self.dtype = dtype
        self.max_num_seqs = max_num_seqs
        self.max_num_batched_tokens = max_num_batched_tokens
        self.context_length = context_length
        self.extra_args = extra_args or []
        self.env = os.environ.copy()
        if env:
            self.env.update(env)
        self._p: Optional[subprocess.Popen] = None

    def start(self, wait_timeout_s: float = 120.0):
        if _is_port_open(self.host, self.port):
            # 端口已被占用：默认认为已有 server 在跑，直接使用
            print(f"[SGLang] Port {self.port} already open; will connect to existing server.")
            return

        cmd = [
            sys.executable, "-m", "sglang.launch_server",
            "--model-path", self.model_path,
            "--tokenizer-path", self.tokenizer_path,
            "--host", self.host,
            "--port", str(self.port),
            "--tensor-parallel-size", str(self.tp),
            "--dtype", self.dtype,
        ]
        if self.context_length:
            cmd += ["--context-length", str(self.context_length)]
        cmd += self.extra_args

        print("[SGLang] Launching server via CLI:\n  " + " ".join(cmd))
        # 将 stdout/stderr 继承到父进程，方便你在控制台看到日志
        self._p = subprocess.Popen(cmd, env=self.env)

        # 等待端口开放
        t0 = time.time()
        while time.time() - t0 < wait_timeout_s:
            if self._p.poll() is not None:
                raise RuntimeError(f"SGLang server exited early with code {self._p.returncode}")
            if _is_port_open(self.host, self.port):
                print(f"[SGLang] Server is up at http://{self.host}:{self.port}")
                return
            time.sleep(0.5)
        raise TimeoutError(f"SGLang server did not open port {self.port} within {wait_timeout_s}s")

    def shutdown(self):
        if self._p is None:
            return
        if self._p.poll() is None:
            print("[SGLang] Terminating server process ...")
            try:
                self._p.terminate()
                try:
                    self._p.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    print("[SGLang] Killing server process ...")
                    self._p.kill()
            except Exception as e:
                print(f"[SGLang] Error terminating server: {e}")
        self._p = None

# -------------------- ModelManager --------------------
class ModelManager:
    """
    后端优先使用 SGLang：
      - 在代码中启动 SGLang Server（子进程，非手动命令）
      - 用 RuntimeEndpoint 连接
    若导入失败或启动失败则回退到 Transformers。
    """
    def __init__(self, num_gpus: int = None, use_sglang: bool = None):
        ModelConfig.validate_config()
        self.model_path = ModelConfig.get_model_path()
        self.tokenizer_path = ModelConfig.get_tokenizer_path()

        self.num_gpus = (torch.cuda.device_count() if (num_gpus is None and torch.cuda.is_available()) else (num_gpus or 1))
        self.use_sglang = (SGLANG_AVAILABLE if use_sglang is None else bool(use_sglang and SGLANG_AVAILABLE))

        if self.use_sglang:
            try:
                print("[Init] Using SGLang backend (code-launched server).")
                self._init_sglang()
                return
            except Exception as e:
                print(f"[Warn] SGLang init failed: {e}\n[Init] Falling back to Transformers.")
        self._init_transformers()

    # ---------- Transformers fallback ----------
    def _init_transformers(self):
        import torch._dynamo as dynamo
        dynamo.config.disable = True
        torch._dynamo.config.disable = True

        self.models = []
        self.tokenizers = []
        self.model_locks = []
        self.request_queue = queue.Queue()
        self.worker_thread = None

        print(f"[Load] Loading {self.num_gpus} HF copies on {self.num_gpus} GPU(s)...")
        for gpu_id in range(self.num_gpus):
            device = f"cuda:{gpu_id}" if torch.cuda.is_available() else "cpu"
            tok = AutoTokenizer.from_pretrained(self.tokenizer_path, trust_remote_code=True)
            if tok.pad_token is None:
                tok.pad_token = tok.eos_token
            model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                torch_dtype=torch.float16 if "cuda" in device else torch.float32,
                device_map=device,
                trust_remote_code=True,
                attn_implementation="eager",
                low_cpu_mem_usage=True,
                use_cache=True,
                _fast_init=False,
            )
            self.models.append(model)
            self.tokenizers.append(tok)
            self.model_locks.append(threading.Lock())
        print("[Load] HF models ready.")

        self.worker_thread = threading.Thread(target=self._model_worker_transformers, daemon=True)
        self.worker_thread.start()
        print("[Worker] Transformers worker started.")

    def _model_worker_transformers(self):
        rr = 0
        while True:
            req = self.request_queue.get()
            if req is None:
                break
            messages, resp_q = req
            gpu_id = rr % len(self.models)
            rr += 1
            try:
                with self.model_locks[gpu_id]:
                    model = self.models[gpu_id]
                    tok = self.tokenizers[gpu_id]
                    formatted = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
                    inputs = tok(formatted, return_tensors="pt", padding=True, truncation=True).to(model.device)
                    with torch.no_grad():
                        out = model.generate(
                            **inputs,
                            max_new_tokens=1024,
                            temperature=0.7,
                            do_sample=True,
                            pad_token_id=tok.eos_token_id,
                        )
                    resp = selective_decode(tok, out[0][inputs["input_ids"].shape[1]:]).strip()
                resp_q.put(resp)
            except Exception as e:
                resp_q.put({"error": str(e)})

    # ---------- SGLang fast path (code-launched) ----------
    def _init_sglang(self):
        # 1) 启动子进程 server
        host = getattr(ModelConfig, "get_sglang_host", lambda: None)() or "127.0.0.1"
        port = getattr(ModelConfig, "get_sglang_port", lambda: None)() or 30000
        dtype = getattr(ModelConfig, "get_dtype", lambda: None)() or "float16"
        max_num_seqs = getattr(ModelConfig, "get_max_num_seqs", lambda: None)() or 512
        max_num_batched_tokens = getattr(ModelConfig, "get_max_num_batched_tokens", lambda: None)() or 8192
        context_length = getattr(ModelConfig, "get_context_length", lambda: None)()

        # 可在 ModelConfig 里暴露额外参数（例如 --load-format, --kv-cache-dtype 等），这里允许透传
        extra_args = getattr(ModelConfig, "get_sglang_extra_args", lambda: None)() or []

        self._sg_proc = SGLangServerProc(
            model_path=self.model_path,
            tokenizer_path=self.tokenizer_path,
            host=host,
            port=port,
            tensor_parallel_size=max(1, self.num_gpus),
            dtype=dtype,
            max_num_seqs=max_num_seqs,
            max_num_batched_tokens=max_num_batched_tokens,
            context_length=context_length,
            extra_args=extra_args,
        )
        self._sg_proc.start(wait_timeout_s=180.0)

        # 2) 连接 endpoint
        self.tokenizer = AutoTokenizer.from_pretrained(self.tokenizer_path, trust_remote_code=True)
        server_url = f"http://{host}:{port}"
        print(f"[SGLang] Connecting endpoint: {server_url}")
        self._sg_endpoint = RuntimeEndpoint(server_url)

        # 3) 启动 worker
        self.request_queue = queue.Queue()
        self.worker_thread = threading.Thread(target=self._model_worker_sglang, daemon=True)
        self.worker_thread.start()
        print("[Worker] SGLang worker started.")

    def _model_worker_sglang(self):
        while True:
            req = self.request_queue.get()
            if req is None:
                break
            messages, resp_q = req
            try:
                formatted = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
                try:
                    resp = self._sg_endpoint.generate(
                        formatted,
                        sampling_params=dict(
                            # max_new_tokens=2048,
                            # temperature=0.8,
                            stop=["<|im_end|>", "<|end_header_id|>", "<end_of_turn>"],
                        ),
                        # stream=False,
                    )
                except TypeError:
                    resp = self._sg_endpoint.generate(
                        formatted,
                        # max_new_tokens=2048,
                        # temperature=0.8,
                        # stop=["<|im_end|>", "<|end_of_turn>"],
                        # stream=False,
                    )
                text = resp["text"] if isinstance(resp, dict) and "text" in resp else str(resp)
                resp_q.put(text.strip())
            except Exception as e:
                resp_q.put({"error": str(e)})

    # ---------- Common API ----------
    def get_least_loaded_gpu(self) -> int:
        return 0

    async def generate_response(self, messages: List[Dict[str, str]]) -> str:
        resp_q = queue.Queue()
        self.request_queue.put((messages, resp_q))
        resp = resp_q.get()
        if isinstance(resp, dict) and "error" in resp:
            raise Exception(resp["error"])
        return resp

    def shutdown(self):
        print("[Shutdown] Stopping model manager ...")
        try:
            self.request_queue.put(None)
            if hasattr(self, "worker_thread") and self.worker_thread:
                self.worker_thread.join(timeout=5)
        except Exception as e:
            print(f"[Shutdown] worker: {e}")

        # 关闭子进程 server
        if hasattr(self, "_sg_proc") and self._sg_proc:
            self._sg_proc.shutdown()
        print("[Shutdown] Done.")

# 全局实例
_model_manager: Optional[ModelManager] = None
def get_model_manager(use_sglang: bool = None) -> ModelManager:
    global _model_manager
    if _model_manager is None:
        num_gpus = torch.cuda.device_count() if torch.cuda.is_available() else 1
        _model_manager = ModelManager(num_gpus=num_gpus, use_sglang=use_sglang if use_sglang is not None else True)
    return _model_manager
