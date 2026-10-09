from typing import Any


class MoviesClient:
    def __init__(self, tmdb_client) -> None:
        self.tmdb_client = tmdb_client

    async def discover_movies(
        self, page: int = 1, release_year: int | None = None
    ) -> dict[str, Any]:

        params: dict[str, int] = {"page": page}

        if release_year is not None:
            params["primary_release_year"] = release_year
        response = await self.tmdb_client.get(
            "/discover/movie",
            params=params,
        )

        return response.json()
