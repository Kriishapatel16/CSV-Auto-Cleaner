import json
import shutil
import time
import uuid
from pathlib import Path


class SessionManager:

    def __init__(self, base_dir, ttl_seconds=1800):
        self.base_dir = Path(base_dir).resolve()
        self.ttl_seconds = int(ttl_seconds)

        if self.ttl_seconds <= 0:
            raise ValueError("Session TTL must be greater than zero.")

        self.base_dir.mkdir(parents=True, exist_ok=True)

    def create_session(self, extension, original_filename=None, size=0):
        session_id = str(uuid.uuid4())
        session_path = self.base_dir / session_id

        session_path.mkdir(parents=True, exist_ok=False)

        now = time.time()

        meta = {
            "session_id": session_id,
            "extension": str(extension).lower().lstrip("."),
            "working_extension": str(extension).lower().lstrip("."),
            "original_filename": original_filename or f"dataset.{extension}",
            "size": int(size or 0),
            "created_at": now,
            "last_activity": now,
            "history": []
        }

        self._write_meta(session_path, meta)

        return session_id

    def get_session_path(self, session_id):
        if not self._valid_session_id(session_id):
            return None

        path = self.base_dir / str(session_id)

        if not path.is_dir():
            return None

        try:
            path.resolve().relative_to(self.base_dir)
        except ValueError:
            return None

        meta = self._read_meta(path)

        if meta is None:
            return None

        last_activity = self._get_last_activity(meta)

        if time.time() - last_activity > self.ttl_seconds:
            self.delete_session(session_id)
            return None

        return path

    def get_meta(self, session_id):
        if not self._valid_session_id(session_id):
            return None

        path = self.base_dir / str(session_id)

        if not path.is_dir():
            return None

        try:
            path.resolve().relative_to(self.base_dir)
        except ValueError:
            return None

        return self._read_meta(path)

    def update_meta(self, session_id, **updates):
        path = self.get_session_path(session_id)

        if path is None:
            return False

        meta = self._read_meta(path)

        if meta is None:
            return False

        meta.update(updates)
        meta["last_activity"] = time.time()

        self._write_meta(path, meta)

        return True

    def touch(self, session_id):
        path = self.get_session_path(session_id)

        if path is None:
            return False

        meta = self._read_meta(path)

        if meta is None:
            return False

        meta["last_activity"] = time.time()
        self._write_meta(path, meta)

        return True

    def delete_session(self, session_id):
        if not self._valid_session_id(session_id):
            return False

        path = self.base_dir / str(session_id)

        if not path.is_dir():
            return False

        try:
            path.resolve().relative_to(self.base_dir)
        except ValueError:
            return False

        try:
            shutil.rmtree(path)
            return True
        except OSError:
            return False

    def cleanup_expired(self):
        if not self.base_dir.exists():
            return 0

        now = time.time()
        deleted = 0

        for path in list(self.base_dir.iterdir()):
            if not path.is_dir():
                continue

            meta = self._read_meta(path)

            if meta is None:
                try:
                    shutil.rmtree(path)
                    deleted += 1
                except OSError:
                    pass
                continue

            last_activity = self._get_last_activity(meta)

            if now - last_activity > self.ttl_seconds:
                try:
                    shutil.rmtree(path)
                    deleted += 1
                except OSError:
                    pass

        return deleted

    def _read_meta(self, path):
        meta_path = Path(path) / "meta.json"

        if not meta_path.is_file():
            return None

        try:
            with meta_path.open("r", encoding="utf-8") as file:
                meta = json.load(file)

            if not isinstance(meta, dict):
                return None

            return meta

        except (OSError, json.JSONDecodeError, TypeError):
            return None

    @staticmethod
    def _get_last_activity(meta):
        try:
            value = meta.get(
                "last_activity",
                meta.get("created_at", 0)
            )
            return float(value)
        except (TypeError, ValueError):
            return 0

    @staticmethod
    def _valid_session_id(session_id):
        try:
            value = str(session_id)
            parsed = uuid.UUID(value)
            return str(parsed) == value.lower()
        except (ValueError, AttributeError, TypeError):
            return False

    @staticmethod
    def _write_meta(path, meta):
        path = Path(path)
        meta_path = path / "meta.json"
        temp_path = path / "meta.json.tmp"

        with temp_path.open("w", encoding="utf-8") as file:
            json.dump(
                meta,
                file,
                indent=2,
                ensure_ascii=False
            )
            file.flush()

        temp_path.replace(meta_path)