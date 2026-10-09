from pydantic_settings import BaseSettings


class ExtractionCheckpoint(BaseSettings):
    job: str
    last_completed_page: int
    total_pages: int
