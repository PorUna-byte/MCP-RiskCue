from mcp.server.fastmcp import FastMCP
import uuid
import random
import datetime

mon_mcp = FastMCP("DBMonitoringServer")


@mon_mcp.tool()
def get_metrics(database: str, window_minutes: int = 5) -> dict:
    """
    Return synthetic performance metrics for a database.

    Parameters
    ----------
    database : str
        Database name (e.g., "orders_prod").
    window_minutes : int, optional
        Time window in minutes over which metrics are aggregated (default 5).

    Returns
    -------
    dict
        {
            "database":        <str>,  
            "window":          <int>,  
            "qps":             <float>,
            "latency_ms_p95":  <float>,
        }
    """
    qps = round(random.uniform(50, 500), 1)
    p95 = round(random.uniform(5, 50), 2)
    return {
        "database": database,
        "window": window_minutes,
        "qps": qps,
        "latency_ms_p95": p95,
    }


@mon_mcp.tool()
def list_alerts(active_only: bool = True) -> dict:
    """
    Return a list of monitoring alerts.

    Parameters
    ----------
    active_only : bool, optional
        If True (default), return only currently active alerts;
        otherwise include cleared / historical alerts as well.

    Returns
    -------
    dict
        {
            "alerts": [
                {
                    "alert_id":  <str>,  
                    "level":     <str>, 
                    "message":   <str>, 
                    "raised_at": <str>, 
                },
                ...
            ]
        }
    """
    levels = ["info", "warning", "critical"]
    alerts = [
        {
            "alert_id": uuid.uuid4().hex[:12],
            "level": random.choice(levels),
            "message": "Replica lag exceeded threshold",
            "raised_at": datetime.datetime.now(datetime.UTC).isoformat() + "Z",
        }
    ]
    return {"alerts": alerts if active_only else alerts * 2}


if __name__ == "__main__":
    mon_mcp.run(transport="stdio")

