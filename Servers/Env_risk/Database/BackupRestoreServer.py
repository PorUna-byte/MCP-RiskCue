from mcp.server.fastmcp import FastMCP
import uuid
import datetime

br_mcp = FastMCP("BackupRestoreServer")


@br_mcp.tool()
def create_backup(database: str) -> dict:
    """
    Start a full backup of the given database.

    Parameters
    ----------
    database : str
        Name of the database to back up (e.g., "sales_prod").

    Returns
    -------
    dict
        {
            "backup_id":  <str>,  
            "created_at": <str>,
        }
    """
    return {
        "backup_id": uuid.uuid4().hex,
        "created_at": datetime.datetime.now(datetime.UTC).isoformat() + "Z",
    }


@br_mcp.tool()
def restore_backup(backup_id: str, target_database: str) -> dict:
    """
    Restore a previously created backup to a target database.

    Parameters
    ----------
    backup_id : str
        ID produced by ``create_backup``.
    target_database : str
        Database that should receive the restore.

    Returns
    -------
    dict
        {
            "restored": <bool>,   
            "target":   <str>, 
        }
    """
    return {"restored": True, "target": target_database}


if __name__ == "__main__":
    br_mcp.run(transport="stdio")


