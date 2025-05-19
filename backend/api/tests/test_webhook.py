import pytest
import requests
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c


def test_submit_item_success(monkeypatch, client):
    # Stub n8n POST
    def fake_post(url, json, auth, timeout):
        class FakeResp:
            status_code = 200
            text = 'ok'
            def raise_for_status(self): pass
        return FakeResp()

    monkeypatch.setattr(requests, 'post', fake_post)
    response = client.post(
        '/submit-item',
        json={'product':'hat','color':'blue'}
    )
    assert response.status_code == 200
    assert response.json['status'] == 'success'