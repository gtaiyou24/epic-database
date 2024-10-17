from injector import singleton, inject

from authority.application.identity.command import RegisterUserCommand, ForgotPasswordCommand, ResetPasswordCommand, \
    ChangePasswordCommand, DeleteUserCommand, SaveUserCommand, LinkAccountCommand, UnlinkAccountCommand
from authority.application.identity.dpo import UserDpo
from authority.application.identity.subscriber import VerificationTokenGeneratedSubscriber, PasswordForgotSubscriber
from authority.domain.model.mail import EmailAddress
from authority.domain.model.user import UserRepository, User, Token, UserId
from authority.domain.model.user.account import OAuthProviderService, Account
from common.application import transactional
from common.domain.model import DomainEventPublisher
from common.exception import SystemException, ErrorCode


@singleton
class IdentityApplicationService:
    @inject
    def __init__(self,
                 oauth_provider_service: OAuthProviderService,
                 user_repository: UserRepository):
        self.oauth_provider_service = oauth_provider_service
        self.user_repository = user_repository

    @transactional
    def register(self, command: RegisterUserCommand) -> UserDpo:
        """ユーザー登録

        ユーザーを登録する際に以下の情報も登録する。また、ユーザーが登録されたときに、メアド検証メールを送信する。

        - ユーザー : 認証/認可の単位となる概念であり、サービスを利用する実体。
        """
        # サブスクライバを登録
        DomainEventPublisher.instance().subscribe(VerificationTokenGeneratedSubscriber())

        # ユーザーを新規作成
        user = User.provision(
            self.user_repository.next_identity(),
            command.user.username,
            EmailAddress(command.user.email_address),
            command.user.plain_password
        )
        if self.user_repository.user_with_email_address(user.email_address):
            raise SystemException(
                ErrorCode.REGISTER_USER_ALREADY_EXISTS,
                f"メールアドレス {user.email_address.text} がすでに登録されています。"
            )

        self.user_repository.add(user)
        return UserDpo(user)

    @transactional
    def verify_email(self, verification_token: str) -> None:
        """メアド検証トークン指定でユーザーを有効化し、セッションを発行する"""
        user = self.user_repository.user_with_token(verification_token)
        token = user.token_with(verification_token)
        if user is None or token.has_expired():
            raise SystemException(ErrorCode.INVALID_TOKEN, f"メアド確認トークン {verification_token} は無効なトークンです。")

        user.verified()
        self.user_repository.add(user)

    @transactional
    def forgot_password(self, command: ForgotPasswordCommand) -> None:
        # サブスクライバを登録
        DomainEventPublisher.instance().subscribe(PasswordForgotSubscriber())

        email_address = EmailAddress(command.email_address)
        user = self.user_repository.user_with_email_address(email_address)
        if user is None:
            raise SystemException(
                ErrorCode.USER_DOES_NOT_FOUND,
                f"{email_address.text} に紐づくユーザーが見つからなかったため、パスワードリセットメールを送信できませんでした。",
            )

        user.generate(Token.Type.PASSWORD_RESET)
        self.user_repository.add(user)

    @transactional
    def reset_password(self, command: ResetPasswordCommand) -> None:
        """新しく設定したパスワードとパスワードリセットトークン指定で新しいパスワードに変更する"""
        user = self.user_repository.user_with_token(command.reset_token)
        if user is None or user.token_with(command.reset_token).has_expired():
            raise SystemException(
                ErrorCode.INVALID_TOKEN,
                f"指定したトークン {command.reset_token} は無効なのでパスワードをリセットできません。",
            )

        user.reset_password(command.password, command.reset_token)
        self.user_repository.add(user)

    @transactional
    def change_password(self, command: ChangePasswordCommand) -> None:
        user = self.user_repository.get(UserId(command.user_id))
        if user is None:
            raise SystemException(ErrorCode.USER_DOES_NOT_FOUND, f"ユーザー {command.user_id} が見つかりません。")

        user.protect_password(command.new_password)
        self.user_repository.add(user)

    def user(self, user_id: str) -> UserDpo:
        user_id = UserId(user_id)
        user = self.user_repository.get(user_id)
        if user is None:
            SystemException(ErrorCode.USER_DOES_NOT_FOUND, f'ユーザー {user_id.value} は見つかりませんでした。')

        return UserDpo(user)

    @transactional
    def save(self, command: SaveUserCommand) -> UserDpo:
        user = self.user_repository.get(UserId(command.user_id))
        if user is None:
            raise SystemException(ErrorCode.USER_DOES_NOT_FOUND, f"ユーザー {command.user_id} は存在しません。")

        user.username = command.username
        user.email_address = EmailAddress(command.email_address)
        self.user_repository.add(user)
        return UserDpo(user)

    @transactional
    def delete(self, command: DeleteUserCommand) -> None:
        user = self.user_repository.get(UserId(command.user_id))
        self.user_repository.remove(user)

    @transactional
    def link(self, command: LinkAccountCommand) -> None:
        _, account = self.oauth_provider_service.authenticate(
            command.provider,
            command.code,
            command.redirect_uri,
            # NOTE: "code_verifier or verifier is not needed." とエラーが発生したため、コメントアウト
            # command.code_verifier,
            None,
            command.grant_type
        )
        user = self.user_repository.get(UserId(command.user_id))
        if user is None:
            raise SystemException(ErrorCode.USER_DOES_NOT_FOUND, f"ユーザー {command.user_id} が見つかりませんでした")

        user.link(account)
        self.user_repository.add(user)

    @transactional
    def unlink(self, command: UnlinkAccountCommand) -> None:
        user = self.user_repository.get(UserId(command.user_id))
        if user is None:
            raise SystemException(ErrorCode.USER_DOES_NOT_FOUND, f"ユーザー {command.user_id} が見つかりませんでした")

        user.unlink(Account.Provider[command.provider])
        self.user_repository.add(user)
