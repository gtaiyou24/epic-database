from injector import singleton, inject

from authority.application.authorization.command import AuthenticateEmailPasswordCommand, RevokeCommand, \
    RefreshCommand, AuthenticateAccountCommand
from authority.application.authorization.dpo import TokenDpo
from authority.application.identity.dpo import UserDpo
from authority.application.identity.subscriber import VerificationTokenGeneratedSubscriber
from authority.domain.model.mail import EmailAddress
from authority.domain.model.token import TokenRepository, BearerToken, RefreshToken
from authority.domain.model.user import UserRepository, Token, User
from authority.domain.model.user.account import OAuthProviderService
from common.application import transactional
from common.domain.model import DomainEventPublisher
from common.exception import SystemException, ErrorCode


@singleton
class AuthorizationApplicationService:
    @inject
    def __init__(self,
                 oauth_provider_service: OAuthProviderService,
                 user_repository: UserRepository,
                 token_repository: TokenRepository):
        self.oauth_provider_service = oauth_provider_service
        self.user_repository = user_repository
        self.token_repository = token_repository

    @transactional
    def authenticate(self, command: AuthenticateEmailPasswordCommand) -> TokenDpo | None:
        """ユーザー認証し、アクセストークン、リフレッシュトークンを発行する"""
        user = self.user_repository.user_with_email_address(EmailAddress(command.email_address))
        # 該当ユーザーが存在するか、パスワードは一致しているか
        if user is None or not user.verify_password(command.plain_password):
            raise SystemException(
                ErrorCode.AUTHORIZATION_FAILURE,
                f"メールアドレス {command.email_address} のユーザーが見つかりませんでした。"
            )

        # メールアドレス検証が終わっていない場合は、確認メールを再送信する
        if not user.is_verified():
            # 認証メール送信のためにサブスクライバを登録
            DomainEventPublisher.instance().subscribe(VerificationTokenGeneratedSubscriber())

            user.generate(Token.Type.VERIFICATION)
            self.user_repository.add(user)
            return None

        access_token, refresh_token = user.login()
        self.token_repository.add(access_token)
        self.token_repository.add(refresh_token)

        return TokenDpo(access_token, refresh_token)

    @transactional
    def authenticate_with_account(self, command: AuthenticateAccountCommand) -> TokenDpo | None:
        profile, account = self.oauth_provider_service.authenticate(
            command.provider,
            command.code,
            command.redirect_uri,
            command.code_verifier,
            command.grant_type
        )
        user = (
            self.user_repository.user_with_account(account.provider, account.provider_account_id) or
            self.user_repository.user_with_email_address(profile.email_address)
        )

        if not user:
            # ユーザーが存在しない場合は、ユーザーを新規作成する
            user = User.provision(self.user_repository.next_identity(),
                                  profile.username,
                                  profile.email_address,
                                  None,
                                  account)

        # すでにユーザーが存在する場合は、認証完了とする
        if not user.is_verified():
            user.verified()

        self.user_repository.add(user)

        access_token, refresh_token = user.login()
        self.token_repository.add(access_token)
        self.token_repository.add(refresh_token)

        return TokenDpo(access_token, refresh_token)

    @transactional
    def refresh(self, command: RefreshCommand) -> TokenDpo:
        """リフレッシュトークン指定で新しいアクセストークンとリフレッシュトークンを取得できる"""
        refresh_token: RefreshToken | None = self.token_repository.token_with_value(command.refresh_token)
        if refresh_token is None or refresh_token.type_is('ACCESS') or refresh_token.is_expired():
            raise SystemException(ErrorCode.INVALID_TOKEN, f"リフレッシュトークン {command.refresh_token} は無効です。")

        new_access_token, new_refresh_token = refresh_token.refresh()

        self.token_repository.add(new_access_token)
        self.token_repository.add(new_refresh_token)

        self.token_repository.remove(refresh_token)

        return TokenDpo(new_access_token, new_refresh_token)

    @transactional
    def revoke(self, command: RevokeCommand) -> None:
        """リフレッシュトークンもしくはアクセストークン指定で、トークンを削除できる

        詳細な仕様は、https://tex2e.github.io/rfc-translater/html/rfc7009.html を参照してください。
        """
        token: BearerToken | None = self.token_repository.token_with_value(command.token)
        if token is not None:
            self.token_repository.remove(token)

        other_token: BearerToken | None = self.token_repository.token_with_value(token.pair_token)
        if other_token is not None:
            self.token_repository.remove(other_token)

    def identify(self, access_token: str) -> UserDpo | None:
        """アクセストークン指定でユーザー情報を取得できる"""
        token: BearerToken | None = self.token_repository.token_with_value(access_token)
        if token is None or token.type_is('REFRESH'):
            raise SystemException(ErrorCode.INVALID_TOKEN, f"アクセストークン {access_token} は無効です。")

        user = self.user_repository.get(token.user_id)
        if user is None:
            raise SystemException(ErrorCode.INVALID_TOKEN, f"アクセストークン {access_token} は無効です。")
        return UserDpo(user)
