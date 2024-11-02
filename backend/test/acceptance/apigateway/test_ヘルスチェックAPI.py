from httpx import Response

from fastapi.testclient import TestClient

import api


class Test_ヘルスチェックAPI:
    client = TestClient(app=api.app)

    def test_ヘルスチェックが確認できる(self):
        r: Response = self.client.get("/health/check")
        assert r.status_code == 200
        assert r.json() == {"health": True}
