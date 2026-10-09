import httpx


class HttpClient:
    def __init__(
        self,
        base_url: str,
        headers: dict[str, str] | None = None,
        timeout: float = 30.0,
    ) -> None:
        self.client = httpx.AsyncClient(
            base_url=base_url, headers=headers, timeout=timeout
        )

    async def get(
        self,
        path: str,
        params: dict[str, str] | None = None,
    ) -> httpx.Response:
        response = await self.client.get(path, params=params)

        if response.is_error:
            print(f"HTTP {response.status_code} for {response.request.url}")
        print(response.text)
        response.raise_for_status()

        return response
