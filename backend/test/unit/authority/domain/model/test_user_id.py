import uuid

import pytest

from authority.domain.model.user import UserId


class TestUserId:
    class Test_生成について:
        def test_UUIDの文字列指定で生成できる(self) -> None:
            try:
                UserId(str(uuid.uuid4()))
            except Exception as e:
                pytest.fail(e)

        @pytest.mark.parametrize("value", [None, '', 'xxxx'])
        def test_UUID以外の文字列を指定するとAsssertionErrorを送出する(self, value) -> None:
            with pytest.raises(AssertionError):
                UserId(value)
