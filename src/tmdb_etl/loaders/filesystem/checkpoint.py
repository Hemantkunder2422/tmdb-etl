import json
from pathlib import Path

from tmdb_etl.model.checkpoint import ExtractionCheckpoint


class FileCheckPointStore:
    def __init__(self, base_path: Path) -> None:
        self.base_path = base_path

    def load(self, job: str) -> ExtractionCheckpoint | None:

        checkpoint_path = self.base_path / f"{job}.json"

        if not checkpoint_path.exists():
            return None

        data = json.loads(checkpoint_path.read_text(encoding="utf-8"))

        return ExtractionCheckpoint.model_validate(data)

    def save(self, checkpoint: ExtractionCheckpoint) -> None:

        self.base_path.mkdir(parents=True, exist_ok=True)

        checkpoint_path = self.base_path / f"{checkpoint.job}.json"

        checkpoint_path.write_text(
            checkpoint.model_dump_json(indent=4), encoding="utf-8"
        )
