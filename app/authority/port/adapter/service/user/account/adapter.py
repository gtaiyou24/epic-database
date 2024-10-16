from __future__ import annotations

import abc
import datetime
import urllib
from enum import Enum
from typing import override, Callable, TypedDict

import requests
from di import DIContainer

from authority.domain.model.mail import EmailAddress
from authority.domain.model.user.account import Account, ProviderTokens, Profile
from common.exception import SystemException, ErrorCode


class OAuthProviderAdapter(abc.ABC):
    class Provider(Enum):
        GOOGLE = ('google', lambda: DIContainer.instance().resolve(GoogleAdapter))

        def __init__(self, provider_name: str, adapter: Callable[[], OAuthProviderAdapter]):
            self.provider_name = provider_name
            self.adapter = adapter

        def authenticate(self, code: str, redirect_uri: str, code_verifier: str | None, grant_type: str) -> (Profile, Account):
            return self.adapter().authenticate(code, redirect_uri, code_verifier, grant_type)

    @abc.abstractmethod
    def authenticate(self, code: str, redirect_uri: str, code_verifier: str, grant_type: str) -> (Profile, Account):
        pass


class GoogleAdapter(OAuthProviderAdapter):
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    @override
    def authenticate(self, code: str, redirect_uri: str, code_verifier: str | None, grant_type: str) -> (Profile, Account):
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": grant_type,
            "redirect_uri": redirect_uri,
        }
        if code_verifier is not None:
            data['code_verifier'] = code_verifier

        # 一時コード指定で Google からアクセストークンを取得する
        # https://developers.google.com/identity/protocols/oauth2/web-server?hl=ja#httprest_3
        token_response = requests.post(
            "https://oauth2.googleapis.com/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=urllib.parse.urlencode(data),
        )
        if not token_response.ok:
            raise SystemException(
                ErrorCode.LINK_ACCOUNT_FAILURE,
                f'Google からアクセストークンを取得できませんでした。詳細: {token_response.json()}'
            )

        token_json: GoogleTranslator.TokenJson = token_response.json()

        userinfo_response = requests.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Content-Type": "application/json"},
            params={"access_token": token_json['access_token']}
        )
        if not userinfo_response.ok:
            raise SystemException(ErrorCode.LINK_ACCOUNT_FAILURE, f'Google からアカウント情報を取得できませんでした')

        return GoogleTranslator.to_account_from(token_json, userinfo_response.json())


class GoogleTranslator:
    class TokenJson(TypedDict):
        access_token: str
        refresh_token: str | None
        scope: str
        id_token: str
        expires_in: int

    class UserInfoJson(TypedDict):
        id: str
        email: str
        name: str
        picture: str

    @staticmethod
    def to_account_from(token: TokenJson, userinfo: UserInfoJson) -> (Profile, Account):
        return (
            Profile(
                userinfo.get('name'),
                EmailAddress(userinfo.get('email')),
                userinfo.get('picture')
            ),
            Account.Provider.GOOGLE.make(
                userinfo.get('id'),
                ProviderTokens(
                    token.get('access_token'),
                    token.get('refresh_token'),
                    datetime.datetime.now() + datetime.timedelta(seconds=token['expires_in']),
                    ProviderTokens.TokenType.BEARER
                ),
                token.get('scope'),
                token.get('id_token'),
            )
        )
