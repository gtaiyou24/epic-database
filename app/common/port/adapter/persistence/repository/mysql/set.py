from typing import Any

from sqlalchemy import TypeDecorator, String, Dialect


class SET(TypeDecorator):
    impl = String

    def __init__(self, items: list[str], *args: Any, **kwargs: Any) -> None:
        self.items = items  # SET に含まれる選択肢
        super().__init__(*args, **kwargs)

    def process_bind_param(self, value: list[str] | set[str] | None, dialect: Dialect) -> str | None:
        """
        Python のリストを MySQL に保存する形式に変換 (カンマ区切りの文字列)
        """
        if isinstance(value, list) or isinstance(value, set):
            return ','.join(value)
        elif isinstance(value, str):
            return value
        return None

    def process_result_value(self, value: str | None, dialect: Dialect) -> set[str]:
        """
        MySQL から取り出した値を Python のリストに変換
        """
        if value:
            return set(value.split(','))
        return set()
