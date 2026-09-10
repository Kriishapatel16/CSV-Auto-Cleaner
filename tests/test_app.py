import io
import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_upload_no_file(client):
    response = client.post("/api/upload")
    assert response.status_code == 400
    assert b"No file part" in response.data

def test_upload_invalid_extension(client):
    data = {"file": (io.BytesIO(b"fake image content"), "test.jpg")}
    response = client.post("/api/upload", data=data, content_type="multipart/form-data")
    assert response.status_code == 400
    assert b"Only .csv files are permitted" in response.data

def test_upload_valid_csv(client):
    csv_content = b"col1,col2\nval1,val2\nval3,val4"
    data = {"file": (io.BytesIO(csv_content), "sample.csv")}
    response = client.post("/api/upload", data=data, content_type="multipart/form-data")
    assert response.status_code == 200
    assert b"uploaded and validated successfully" in response.data