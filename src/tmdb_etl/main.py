import asyncio
from pathlib import Path

from tmdb_etl.clients.http.client import HttpClient
from tmdb_etl.clients.tmdb.client import TMDBClient
from tmdb_etl.config.settings import Settings
from tmdb_etl.ingestion.api.extractor import MovieExtracter
from tmdb_etl.ingestion.api.people_extracter import PeopleExtractor
from tmdb_etl.loaders.filesystem.checkpoint import FileCheckPointStore
from tmdb_etl.loaders.filesystem.raw_writer import RawDataWriter


async def run() -> None:
    settings = Settings()

    release_years = [2026]

    data_type = input("enter data type: (movie | tv | people )").lower()

    if data_type not in ["movie", "tv", "people"]:
        raise ValueError("Invalid data type")

    fetched_data_years = []

    http_client = HttpClient(
        base_url=settings.tmdb_base_url,
        headers={
            "Authorization": f"Bearer {settings.tmdb_api_key}",
            "Accept": "application/json",
        },
    )

    checkpoint_store = FileCheckPointStore(
        base_path=Path(f"data/checkpoints/{data_type}")
    )
    raw_writer = RawDataWriter(base_path=Path(f"data/raw/{data_type}"))
    tmdb_client = TMDBClient(http_client=http_client)
    movie_extracter = MovieExtracter(
        tmdb_client=tmdb_client,
        checkpoint_store=checkpoint_store,
        raw_writer=raw_writer,
    )
    people_extractor = PeopleExtractor(
        tmdb_client=tmdb_client,
        checkpoint_store=checkpoint_store,
        raw_writer=raw_writer,
    )

    match data_type:
        case "movie":
            for year in release_years:
                movies = await movie_extracter.extract_movies(
                    page=1, release_year=year, max_page=1
                )
                fetched_data_years.append(year)
            print(f"Total movies extracted: {len(movies)}")
        case "people":
            people = await people_extractor.extract_people(page=501, max_page=3)
            print(f"Total peoples extracted: {len(people)}")


def main() -> None:

    asyncio.run(run())


if __name__ == "__main__":
    main()
