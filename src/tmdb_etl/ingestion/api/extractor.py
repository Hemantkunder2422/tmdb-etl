from typing import Any

from tmdb_etl.clients.tmdb.client import TMDBClient
from tmdb_etl.loaders.filesystem.checkpoint import FileCheckPointStore
from tmdb_etl.loaders.filesystem.raw_writer import RawDataWriter
from tmdb_etl.model.checkpoint import ExtractionCheckpoint


class MovieExtracter:
    def __init__(
        self,
        tmdb_client: TMDBClient,
        checkpoint_store: FileCheckPointStore,
        raw_writer: RawDataWriter,
    ) -> None:

        self.tmdb_client = tmdb_client
        self.checkpoint_store = checkpoint_store
        self.raw_writer = raw_writer

    async def extract_movies(
        self,
        page: int = 1,
        release_year: int | None = None,
        max_page: int | None = None,
    ) -> list[dict[str, Any]]:

        movies: list[dict[str, Any]] = []

        job = f"movie-{release_year}"

        checkpoint = self.checkpoint_store.load(job)

        if checkpoint:
            start_page = checkpoint.last_completed_page + 1

            print(f"Resuming from page {start_page}")

        else:
            start_page = 1

        page = start_page

        while True:
            response = await self.tmdb_client.movie_client.discover_movies(
                page, release_year
            )

            results = response.get("results", [])

            movies.extend(results)

            total_page = 500

            print(f"Fetched page {page}/{total_page}({len(results)} movies)")

            self.raw_writer.write_page(
                dataset=f"movies/{release_year}", page=page, data=response
            )

            self.checkpoint_store.save(
                checkpoint=ExtractionCheckpoint(
                    job=job, last_completed_page=page, total_pages=total_page
                )
            )

            if page >= total_page:
                break

            if max_page is not None and page >= max_page:
                break

            page += 1

        return movies
