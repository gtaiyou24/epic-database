class NotificationReader:
    def __init__(self, json_notification: str):
        self.__json: dict = eval(json_notification)

    def event_str_value(self, keys: str) -> str | None:
        return self.__str_value(keys)

    def event_bool_value(self, keys: str) -> bool | None:
        optional = self.__str_value(keys)
        return None if optional is None else bool(optional)

    def event_int_value(self, keys: str) -> int | None:
        optional = self.__str_value(keys)
        return None if optional is None else int(optional)

    def event_float_value(self, keys: str) -> float | None:
        optional = self.__str_value(keys)
        return None if optional is None else float(optional)

    def __str_value(self, keys: str) -> str | None:
        value = self.__json
        for key in keys.split("."):
            if value is None or key not in value.keys():
                return None
            value = value[key]
        return str(value)
