from typing import Any


class PeopleClient:
    def __init__(self, tmdb_client) -> None:
        self.tmdb_client = tmdb_client

    async def get_peoples(self, page: int = 1) -> dict[str, Any]:

        params: dict[str, int] = {"page": page}

        response = await self.tmdb_client.get(
            "/person/popular",
            params=params,
        )

        return response.json()
