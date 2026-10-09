from typing import Any

from tmdb_etl.clients.http.client import HttpClient
from tmdb_etl.clients.tmdb.movie import MoviesClient
from tmdb_etl.clients.tmdb.people import PeopleClient
from tmdb_etl.clients.tmdb.tv import TvClient


class TMDBClient:
    def __init__(self, http_client: HttpClient) -> None:
        self.http_client = http_client
        self.movie_client = MoviesClient(tmdb_client=http_client)
        self.tv_client = TvClient(tmdb_client=http_client)
        self.people_client = PeopleClient(tmdb_client=http_client)
