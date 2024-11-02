import os
import secrets
from dataclasses import dataclass
from datetime import datetime
from typing import Literal

import jwt
from fastapi import status, Depends, HTTPException
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer, HTTPBasicCredentials, HTTPBasic

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
http_basic = HTTPBasic()


@dataclass(init=True, unsafe_hash=True, frozen=True)
class CurrentUser:
    @dataclass(init=True, unsafe_hash=True, frozen=True)
    class Account:
        @dataclass(init=True, unsafe_hash=True, frozen=True)
        class Tokens:
            access_token: str
            refresh_token: str | None
            expires_at: datetime
            token_type: str

        provider: str
        provider_account_id: str
        tokens: Tokens
        scope: str
        id_token: str

        @staticmethod
        def from_(payload: dict) -> 'CurrentUser.Account':
            return CurrentUser.Account(
                provider=payload["provider"],
                provider_account_id=payload["provider_account_id"],
                tokens=CurrentUser.Account.Tokens(
                    access_token=payload['tokens']["access_token"],
                    refresh_token=payload['tokens']["refresh_token"],
                    expires_at=payload['tokens']["expires_at"],
                    token_type=payload['tokens']["token_type"]
                ),
                scope=payload["scope"],
                id_token=payload["id_token"],
            )

    id: str
    accounts: set[Account]

    @staticmethod
    def from_(payload: dict) -> 'CurrentUser':
        return CurrentUser(
            id=payload['user_id'],
            accounts={CurrentUser.Account.from_(account) for account in payload.get('accounts', [])}
        )


@dataclass(frozen=True, eq=True)
class GetCurrentUser:
    """内部通信用トークンからアクセスユーザー情報を取得する

    Usage:

    def get(self, current_user: CurrentUser = Depends(GetCurrentUser(permit={'ADMIN'}))):
        ...
    """
    permit: set[Literal['ALL', 'OWNER', 'ADMIN', 'EDITOR', 'VIEWER']]

    def __call__(self, request: Request, token: str = Depends(oauth2_scheme)) -> CurrentUser:
        internal_token = request.headers.get('x-internal-token')
        # 内部通信用トークンを署名検証し、ユーザー情報を取得する
        payload = jwt.decode(
            internal_token,
            key="""-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEArgkhiVO4WGp8PUGUU1/a
XKri+E6NTvlxpHNMwSAs/ORU3MlomX/0fOEVW7qA/G0EEl8UgkfzuJhIpMrZP9EP
pEt4LZpcRwbYjdQYnImxWajbhmduZATmbdqjSVuA+NvIk2rIvtQ+aoVShjMetsU+
rwWUUYk164hY3fJezH7FSb2rVXzwWhEon30iSDKEE2o90aK8jSLheok5bPi0AMAs
FtRayuvuVWsKauW0FndvM6hsHTSYqs/D1VQFpuQCiz2mcElWwSP15GxQ4lBnUt/i
/n0yu41lDI58OlZwtkzejlgXc1hGy+8SEkIAxVqi0vzBhHiDvpsaymQDNqv9tkjI
ihuYPBT1Mfwomlox6f3LyDsh3EBTFKf6CnfhbYljNEwczrHSREHAkJwzB7NTtziv
Bu0K8ydi3t8XXvnLcq5xxcusjEOHx6a/7juoONJ2WRdV/WWEY1O16wP03oMqi5az
NIdlD3z2/inCDBKSOufsEUP6szCErQWHWt/S0xfuu3dAFpME8/ELVN+Vjnw7XsSW
YqYxaD/FwXEl9AgFGCWOOKChg6vim97ymE+p3ljeLbam7/jlQDFPYMxNAi3cI8is
NzzW09udb5TzqDxWb0+o7bdx+C043b3hQpZgszcDjKNE3BQGt51krFxZemNWRkhd
/MwSdUE8hTqT6jftw4VD+GUCAwEAAQ==
-----END PUBLIC KEY-----""",  # 一旦ハードコードで実装
            verify=True,
            audience=str(request.url),
            algorithms=["RS256"]
        )
        # TODO: 取得したユーザー情報をもとに必要な権限を有しているのか確認する。もし必要な権限を持っていない場合は 403 とする。
        return CurrentUser.from_(payload)

    def __hash__(self) -> int:
        return hash(",".join(sorted(map(str, list(self.permit)))))


@dataclass(init=False, frozen=True, eq=True)
class AuthenticateAdminUser:
    """サービス管理者情報を取得する

    主にデータの削除や更新など一般ユーザーが利用できないようにしたいエンドポイントに対して指定します。
    """
    username: str
    password: str
    allowed_ip_addresses: list[str]

    def __init__(self,
                 username: str | None = None,
                 password: str | None = None,
                 allowed_ip_addresses: list[str] = []):
        super().__setattr__("username", username or 'uibakery')
        super().__setattr__("password", password or os.getenv('ADMIN_PASSWORD', 'password'))
        super().__setattr__("allowed_ip_addresses",
                            allowed_ip_addresses or os.getenv('ADMIN_API_ALLOWED_IP_ADDRESSES', '127.0.0.1').split(','))

    def __hash__(self) -> int:
        return hash(f"{self.username}{self.password}{','.join(self.allowed_ip_addresses)}")

    def __call__(self, request: Request, credentials: HTTPBasicCredentials = Depends(http_basic)) -> None:
        correct_username = secrets.compare_digest(credentials.username, self.username)
        correct_password = secrets.compare_digest(credentials.password, self.password)
        if not (correct_username and correct_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Basic"},
            )
        # 現時点ではUI Bakeryからのみのアクセスを想定している
        if request.headers.getlist("X-Forwarded-For"):
            ip = request.headers.getlist("X-Forwarded-For")[0].split(',')[0].strip()
        else:
            ip = request.client.host
        if ip not in self.allowed_ip_addresses:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"IP {ip} is not correct",
                headers={"WWW-Authenticate": "Basic"},
            )
