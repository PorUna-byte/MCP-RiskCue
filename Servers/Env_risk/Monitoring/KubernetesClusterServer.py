from mcp.server.fastmcp import FastMCP
import uuid, random

k8s_mcp = FastMCP("KubernetesClusterServer")

@k8s_mcp.tool()
def pod_status(namespace: str, limit: int = 10) -> dict:
    """
    List random pod statuses in a namespace.

    Parameters
    ----------
    namespace : str
    limit : int, optional

    Returns
    -------
    dict
        {"namespace": <str>, "pods": [ {"name": <str>, "state": <str>}, … ]}
    """
    states = ["Running", "Pending", "CrashLoopBackOff"]
    pods = [{"name": f"pod-{i}", "state": random.choice(states)} for i in range(limit)]
    return {"namespace": namespace, "pods": pods}


if __name__ == "__main__":
    k8s_mcp.run(transport="stdio")
