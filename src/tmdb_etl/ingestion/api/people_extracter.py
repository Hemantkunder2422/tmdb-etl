from typing import Any

import httpx

from tmdb_etl.clients.tmdb.client import TMDBClient
from tmdb_etl.loaders.filesystem.checkpoint import FileCheckPointStore
from tmdb_etl.loaders.filesystem.raw_writer import RawDataWriter
from tmdb_etl.model.checkpoint import ExtractionCheckpoint


class PeopleExtractor:
    def __init__(
        self,
        tmdb_client: TMDBClient,
        checkpoint_store: FileCheckPointStore,
        raw_writer: RawDataWriter,
    ) -> None:

        self.tmdb_client = tmdb_client
        self.checkpoint_store = checkpoint_store
        self.raw_writer = raw_writer

    async def extract_people(
        self,
        page: int = 1,
        max_page: int | None = None,
    ) -> list[dict[str, Any]]:

        job = f"people-{page}"

        peoples: list[dict[str, Any]] = []

        checkpoint = self.checkpoint_store.load(job)

        if checkpoint:
            start_page = checkpoint.last_completed_page + 1
            print(f"Resuming from page {start_page}")
        else:
            start_page = 1

        page = start_page

        while True:
            try:
                response = await self.tmdb_client.people_client.get_peoples(page=501)
                results = response.get("results", [])

                peoples.extend(results)

                total_pages = response.get("total_pages", 1)

                print(f"Fetched page {page}/{total_pages}({len(results)} movies)")

                self.raw_writer.write_page(dataset="peoples", page=page, data=response)
                self.checkpoint_store.save(
                    checkpoint=ExtractionCheckpoint(
                        job=job, last_completed_page=page, total_pages=total_pages
                    )
                )

                if page >= total_pages:
                    break

                if max_page is not None and page >= max_page:
                    break

                page += 1
            except httpx.HTTPError as e:
                print(e)
                break

        return peoples
