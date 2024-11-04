import io
import json
import zipfile
from typing import override

import requests
from tqdm import tqdm
from slf4py import set_logger

from common.exception import SystemException, ErrorCode
from common.port.adapter.messaging import ExchangeListener


@set_logger
class DownloadGBizINFOListener(ExchangeListener):
    @override
    def filtered_dispatch(self, event_type: str, text_message: str) -> None:
        self.log.debug("gBizINFO から法人データをダウンロード中...")
        response = requests.post(
            'https://info.gbiz.go.jp/hojin/DownloadJson',
            headers={'Content-Type': 'application/json'}
        )
        if not response.ok:
            raise SystemException(
                ErrorCode.DOWNLOAD_DATA_FAILED, f"gBizINFO から法人データをダウンロードするのに失敗しました")

        self.log.debug("ダウンロード完了!")

        with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
            for path in tqdm(zf.namelist()):
                with zf.open(path) as f:
                    payload = json.loads(f.read())
                    print(payload)

    @override
    def publisher_name(self) -> str:
        return "scheduler"

    @override
    def listens_to(self, event_type: str) -> bool:
        return event_type in ["DownloadgBizINFO.1"]
