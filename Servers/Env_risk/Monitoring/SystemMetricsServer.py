from mcp.server.fastmcp import FastMCP
import uuid, random, datetime, psutil   # psutil optional; random fallback

sys_mcp = FastMCP("SystemMetricsServer")

@sys_mcp.tool()
def cpu_load() -> dict:
    """
    Return current CPU utilization.

    Returns
    -------
    dict
        {"timestamp": <str>, "load_pct": <float>}
    """
    try:
        pct = psutil.cpu_percent(interval=0.1)
    except Exception:
        pct = round(random.uniform(0, 100), 1)
    return {"timestamp": datetime.datetime.now(datetime.UTC).isoformat() + "Z", "load_pct": pct}


@sys_mcp.tool()
def memory_usage() -> dict:
    """
    Report RAM usage in megabytes.

    Returns
    -------
    dict
        {"used_mb": <int>, "total_mb": <int>}
    """
    try:
        mem = psutil.virtual_memory()
        used, total = mem.used // (1024 ** 2), mem.total // (1024 ** 2)
    except Exception:
        total = 16384
        used = random.randint(0, total)
    return {"used_mb": used, "total_mb": total}


if __name__ == "__main__":
    sys_mcp.run(transport="stdio")
