from httpx import Response

from fastapi.testclient import TestClient

from app import main


class Test_ヘルスチェックAPI:
    client = TestClient(app=main.app)

    def test_ヘルスチェックが確認できる(self):
        r: Response = self.client.get("/health/check")
        assert r.status_code == 200
        assert r.json() == {"health": True}
