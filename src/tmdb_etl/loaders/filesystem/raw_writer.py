import json
from pathlib import Path
from typing import Any


class RawDataWriter:
    def __init__(self, base_path: Path):
        self.base_path = base_path

    def write_page(
        self,
        dataset: str,
        page: int,
        data: list[dict[str, Any]],
    ) -> None:
        dataset_path = self.base_path / dataset
        dataset_path.mkdir(parents=True, exist_ok=True)
        file_path = dataset_path / f"page_{page:04d}.json"

        file_path.write_text(json.dumps(data, indent=4), encoding="utf-8")
