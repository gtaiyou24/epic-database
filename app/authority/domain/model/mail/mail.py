import os
from dataclasses import dataclass

from authority.domain.model.mail import EmailAddress
from authority.domain.model.user import Token


@dataclass(init=False, unsafe_hash=True, frozen=True)
class Mail:
    to: EmailAddress
    from_: EmailAddress
    subject: str
    html: str

    def __init__(self, to: EmailAddress, from_: EmailAddress, subject: str, html: str):
        assert isinstance(to, EmailAddress), f"宛先には {type(to)} ではなく {type(EmailAddress)} を指定してください。"
        assert isinstance(from_, EmailAddress), f"差出人には {type(to)} ではなく {type(EmailAddress)} を指定してください。"
        assert subject, "メールアドレスのタイトルは必須です。"
        assert html, "メールアドレス本文は必須です。"
        super().__setattr__("to", to)
        super().__setattr__("from_", from_)
        super().__setattr__("subject", subject)
        super().__setattr__("html", html)


class VerificationMail(Mail):
    def __init__(self, to: EmailAddress, verification_token: Token):
        from_ = EmailAddress(os.getenv("FROM_MAIL_ADDRESS"))
        html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>メールアドレス認証</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
  <div style="background: linear-gradient(to right, #4CAF50, #45a049); padding: 20px; text-align: center;">
    <h1 style="color: white; margin: 0;">メールアドレス認証</h1>
  </div>
  <div style="background-color: #f9f9f9; padding: 20px; border-radius: 0 0 5px 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
    <p>この度はご登録ありがとうございました！下記の認証ボタンをクリックし、登録を完了させてください。</p>
    <div style="text-align: center; margin: 30px 0;">
      <span style="font-size: 32px; font-weight: bold; letter-spacing: 5px; color: #4CAF50;">
        <a href="{os.getenv('FRONTEND_URL')}/auth/new-verification?token={verification_token.value}" style="background-color: #4CAF50; color: white; padding: 12px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">メールアドレスを認証</a>
      </span>
    </div>
    <p>10分以内に認証を完了されない場合は、上記のボタンは無効になります。</p>
    <p>もしアカウントを作成していない場合は、本メールを無視してください。</p>
    <p>よろしくお願い致します。<br>サポートチーム</p>
  </div>
  <div style="text-align: center; margin-top: 20px; color: #888; font-size: 0.8em;">
    <p>これは自動メッセージですので、返信しないでください。</p>
  </div>
</body>
</html>"""
        super().__init__(to, from_, "メールアドレスの認証", html)


class PasswordResetMail(Mail):
    def __init__(self, to: EmailAddress, password_reset_token: Token):
        from_ = EmailAddress(os.getenv("FROM_MAIL_ADDRESS"))
        html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>パスワード再設定のご案内</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
  <div style="background: linear-gradient(to right, #4CAF50, #45a049); padding: 20px; text-align: center;">
    <h1 style="color: white; margin: 0;">パスワードの再設定</h1>
  </div>
  <div style="background-color: #f9f9f9; padding: 20px; border-radius: 0 0 5px 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
    <p>ご利用いただきありがとうございます。</p>
    <p>パスワードの再設定依頼を受け付けました。お心当たりのない場合は、本メールを無視もしくは破棄していただきますようお願いします。</p>
    <p>パスワードを再設定するには以下のボタンをクリックしてください。</p>
    <div style="text-align: center; margin: 30px 0;">
      <a href="{os.getenv('FRONTEND_URL')}/auth/new-password?token={password_reset_token.value}" style="background-color: #4CAF50; color: white; padding: 12px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">新しいパスワードを設定</a>
    </div>
    <p>このリンクの有効期限は10分です。</p>
    <p>有効期限を過ぎてしまった場合はお手数ですが、以下のボタンから再度パスワードの再設定をご依頼下さい。</p>
    <div style="text-align: center; margin: 30px 0;">
      <a href="{os.getenv('FRONTEND_URL')}/auth/reset" style="background-color: #4CAF50; color: white; padding: 12px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">パスワードを再設定依頼</a>
    </div>
  </div>
  <div style="text-align: center; margin-top: 20px; color: #888; font-size: 0.8em;">
    <p>This is an automated message, please do not reply to this email.</p>
  </div>
</body>
</html>"""
        super().__init__(to, from_, "パスワード再設定のご案内", html)
