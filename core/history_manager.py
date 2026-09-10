import re
import shutil
from pathlib import Path


class HistoryManager:

    def __init__(self, session_path):
        self.session_path = Path(session_path).resolve()
        self.history_path = self.session_path / "history"

        self.history_path.mkdir(
            parents=True,
            exist_ok=True
        )

    def _snapshots(self):
        files = list(
            self.history_path.glob("snapshot_*.*")
        )

        def number(path):
            match = re.fullmatch(
                r"snapshot_(\d+)",
                path.stem
            )

            return int(match.group(1)) if match else -1

        return sorted(
            files,
            key=number
        )

    def create_snapshot(self, current_file):
        current_file = Path(current_file).resolve()

        if not current_file.is_file():
            raise FileNotFoundError(
                "Current dataset file was not found."
            )

        try:
            current_file.relative_to(
                self.session_path
            )
        except ValueError:
            raise ValueError(
                "Current file must belong to the session."
            )

        snapshots = self._snapshots()

        if snapshots:
            match = re.fullmatch(
                r"snapshot_(\d+)",
                snapshots[-1].stem
            )
            number = (
                int(match.group(1)) + 1
                if match
                else len(snapshots) + 1
            )
        else:
            number = 1

        snapshot = (
            self.history_path /
            f"snapshot_{number}{current_file.suffix.lower()}"
        )

        shutil.copy2(
            current_file,
            snapshot
        )

        return snapshot

    def get_latest_snapshot(self):
        snapshots = self._snapshots()

        return (
            snapshots[-1]
            if snapshots
            else None
        )

    def restore_latest(self, current_file):
        current_file = Path(current_file).resolve()

        try:
            current_file.relative_to(
                self.session_path
            )
        except ValueError:
            raise ValueError(
                "Current file must belong to the session."
            )

        snapshot = self.get_latest_snapshot()

        if snapshot is None:
            return False

        shutil.copy2(
            snapshot,
            current_file
        )

        snapshot.unlink(
            missing_ok=True
        )

        return True

    def clear(self):
        if self.history_path.exists():
            shutil.rmtree(
                self.history_path,
                ignore_errors=True
            )

        self.history_path.mkdir(
            parents=True,
            exist_ok=True
        )