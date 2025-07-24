from mcp.server.fastmcp import FastMCP
import statistics

stat_mcp = FastMCP("StatisticsServer")

@stat_mcp.tool()
def descriptive_stats(values: list[float]) -> dict:
    """
    Return mean and standard deviation.

    Parameters
    ----------
    values : list[float]

    Returns
    -------
    dict
        {"mean": <float>, "stdev": <float>}
    """
    return {"mean": statistics.mean(values), "stdev": statistics.stdev(values) if len(values) > 1 else 0}


if __name__ == "__main__":
    stat_mcp.run(transport="stdio")
