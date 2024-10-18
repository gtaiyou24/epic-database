from typing import Optional


class NotificationReader:
    def __init__(self, json_notification: str):
        self.__json: dict = eval(json_notification)

    def event_str_value(self, keys: str) -> Optional[str]:
        return self.__str_value(keys)

    def event_bool_value(self, keys: str) -> Optional[bool]:
        optional = self.__str_value(keys)
        return None if optional is None else bool(optional)

    def event_int_value(self, keys: str) -> Optional[int]:
        optional = self.__str_value(keys)
        return None if optional is None else int(optional)

    def event_float_value(self, keys: str) -> Optional[float]:
        optional = self.__str_value(keys)
        return None if optional is None else float(optional)

    def __str_value(self, keys: str) -> Optional[str]:
        value = self.__json
        for key in keys.split("."):
            if value is None or key not in value.keys():
                return None
            value = value[key]
        return str(value)
