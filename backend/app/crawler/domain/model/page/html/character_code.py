from enum import Enum


class CharacterCode(Enum):
    UTF_8 = 'utf-8'
    SHIFT_JIS = 'shift-jis'
    EUC_JP = 'euc-jp'
    WINDOWS_1254 = 'windows-1254'

    @staticmethod
    def value_of(char_code: str):
        for e in CharacterCode:
            if e.value.lower() == char_code:
                return e
        return CharacterCode.UTF_8
