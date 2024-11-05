from pydantic import BaseModel, Field


class MessageJson(BaseModel):
    class Message(BaseModel):
        data: str = Field(title="base64エンコーディングしたデータ")

    message: Message
