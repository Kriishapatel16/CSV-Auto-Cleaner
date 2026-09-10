import io

#import pytest

from app import app
from core.session_manager import SessionManager


@pytest.fixture
def client(tmp_path):
    app.config["TESTING"] = True

    app.session_manager = SessionManager(
        tmp_path / "sessions",
        app.config["SESSION_TTL_SECONDS"]
    )

    with app.test_client() as client:
        yield client


def test_upload_no_file(client):
    response = client.post("/api/upload")

    assert response.status_code == 400

    data = response.get_json()

    assert data["success"] is False
    assert data["error"] == "Please select a file to upload."


def test_upload_invalid_extension(client):
    data = {
        "file": (
            io.BytesIO(b"fake image content"),
            "test.jpg"
        )
    }

    response = client.post(
        "/api/upload",
        data=data,
        content_type="multipart/form-data"
    )

    assert response.status_code == 400

    result = response.get_json()

    assert result["success"] is False
    assert "Unsupported file type" in result["error"]


def test_upload_valid_csv(client):
    csv_content = b"col1,col2\nval1,val2\nval3,val4"

    data = {
        "file": (
            io.BytesIO(csv_content),
            "sample.csv"
        )
    }

    response = client.post(
        "/api/upload",
        data=data,
        content_type="multipart/form-data"
    )

    assert response.status_code == 200

    result = response.get_json()

    assert result["success"] is True
    assert result["filename"] == "sample.csv"
    assert result["extension"] == "csv"
    assert result["working_extension"] == "csv"
    assert result["session_id"]