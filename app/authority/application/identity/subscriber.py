from typing import override

from authority.domain.model.mail import SendMailService, VerificationMail, PasswordResetMail
from authority.domain.model.user import VerificationTokenGenerated, UserRepository, PasswordResetTokenGenerated
from common.domain.model import DomainEventSubscriber, DomainRegistry


class VerificationTokenGeneratedSubscriber(DomainEventSubscriber[VerificationTokenGenerated]):
    """ユーザー作成イベントを購読するサブスクライバ"""
    def __init__(self):
        self.send_mail_service = DomainRegistry.resolve(SendMailService)
        self.user_repository = DomainRegistry.resolve(UserRepository)

    @override
    def subscribed_to_event_type(self) -> type[VerificationTokenGenerated]:
        return VerificationTokenGenerated

    @override
    def handle_event(self, domain_event: VerificationTokenGenerated) -> None:
        """メアド確認のための検証メールを送信する"""
        try:
            self.send_mail_service.send(VerificationMail(domain_event.email_address, domain_event.token))
        except Exception as e:
            raise ValueError(f"ユーザー {domain_event.user_id.value} 宛のメールアドレス認証メールを送信できませんでした。{e}")


class PasswordForgotSubscriber(DomainEventSubscriber[PasswordResetTokenGenerated]):
    """パスワードリセットイベントを購読するサブスクライバ"""

    def __init__(self):
        self.send_mail_service = DomainRegistry.resolve(SendMailService)
        self.user_repository = DomainRegistry.resolve(UserRepository)

    @override
    def subscribed_to_event_type(self) -> type[PasswordResetTokenGenerated]:
        return PasswordResetTokenGenerated

    @override
    def handle_event(self, domain_event: PasswordResetTokenGenerated) -> None:
        """メアド確認のための検証メールを送信する"""
        try:
            self.send_mail_service.send(PasswordResetMail(domain_event.email_address, domain_event.token))
        except Exception as e:
            raise ValueError(f"ユーザー {domain_event.user_id.value} 宛のパスワード再設定メールを送信できませんでした。{e}")
