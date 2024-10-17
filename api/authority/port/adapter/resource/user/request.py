from pydantic import BaseModel, Field, model_validator


class RegisterUserRequest(BaseModel):
    username: str = Field(title="ユーザー名")
    email_address: str = Field(title="メールアドレス")
    password: str = Field(title="パスワード")


class ForgotPasswordRequest(BaseModel):
    email_address: str = Field(title="メールアドレス")


class ResetPasswordRequest(BaseModel):
    token: str = Field(title="パスワードリセットトークン")
    password: str = Field(title="パスワード")


class ChangePasswordRequest(BaseModel):
    new_password: str = Field(title="新しいパスワード", min_length=1)
    check_new_password: str = Field(title="確認用の新しいパスワード", min_length=1)

    @model_validator(mode="after")
    def validate_password(self):
        """2つのパスワードが一致しているかをチェックする"""
        if self.new_password != self.check_new_password:
            raise ValueError("passwords do not match")
        return self


class SaveUserRequest(BaseModel):
    username: str = Field(title="ユーザー名")
    email_address: str = Field(title="メールアドレス")
