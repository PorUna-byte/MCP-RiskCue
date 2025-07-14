from mcp.server.fastmcp import FastMCP
import uuid, random

mov_mcp = FastMCP("MovieCatalogServer")

@mov_mcp.tool()
def search_movies(query: str, limit: int = 5) -> dict:
    """
    Search the movie catalog by title substring.

    Parameters
    ----------
    query : str
        Free-text search string.
    limit : int, optional
        Maximum number of hits (default 5).

    Returns
    -------
    dict
        {
            "results": [
                {"imdb_id": <str>, "title": <str>, "year": <int>}, …
            ]
        }
    """
    hits = [
        {"imdb_id": f"tt{random.randint(1000000, 9999999)}",
         "title": f"{query.title()} {i}",
         "year": random.randint(1980, 2025)}
        for i in range(limit)
    ]
    return {"results": hits}


@mov_mcp.tool()
def movie_detail(imdb_id: str) -> dict:
    """
    Fetch extended metadata for one film.

    Parameters
    ----------
    imdb_id : str
        IMDb identifier (e.g., 'tt1234567').

    Returns
    -------
    dict
        {
            "imdb_id" : <str>,
            "title"   : <str>,
            "director": <str>,
            "runtime" : <int>,
            "genres"  : [<str>, …]
        }
    """
    genres = random.sample(["Action", "Comedy", "Drama", "Sci-Fi", "Horror"], k=2)
    return {
        "imdb_id": imdb_id,
        "title": "Sample Movie",
        "director": "Jane Doe",
        "runtime": random.randint(80, 150),
        "genres": genres,
    }


if __name__ == "__main__":
    mov_mcp.run(transport="stdio")
