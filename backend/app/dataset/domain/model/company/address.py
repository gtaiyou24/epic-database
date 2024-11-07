from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Literal


class Prefecture(Enum):
    HOKKAIDO = ('北海道', '01')
    AOMORI = ('青森県', '02')
    IWATE = ('岩手県', '03')
    MIYAGI = ('宮城県', '04')
    AKITA = ('秋田県', '05')
    YAMAGATA = ('山形県', '06')
    FUKUSHIMA = ('福島県', '07')
    IBARAKI = ('茨城県', '08')
    TOCHIGI = ('栃木県', '09')
    GUNMA = ('群馬県', '10')
    SAITAMA = ('埼玉県', '11')
    CHIBA = ('千葉県', '12')
    TOKYO = ('東京都', '13')
    KANAGAWA = ('神奈川県', '14')
    NIIGATA = ('新潟県', '15')
    TOYAMA = ('富山県', '16')
    ISHIKAWA = ('石川県', '17')
    FUKUI = ('福井県', '18')
    YAMANASHI = ('山梨県', '19')
    NAGANO = ('長野県', '20')
    GIFU = ('岐阜県', '21')
    SHIZUOKA = ('静岡県', '22')
    AICHI = ('愛知県', '23')
    MIE = ('三重県', '24')
    SHIGA = ('滋賀県', '25')
    KYOTO = ('京都府', '26')
    OSAKA = ('大阪府', '27')
    HYOGO = ('兵庫県', '28')
    NARA = ('奈良県', '29')
    WAKAYAMA = ('和歌山県', '30')
    TOTTORI = ('鳥取県', '31')
    SHIMANE = ('島根県', '32')
    OKAYAMA = ('岡山県', '33')
    HIROSHIMA = ('広島県', '34')
    YAMAGUCHI = ('山口県', '35')
    TOKUSHIMA = ('徳島県', '36')
    KAGAWA = ('香川県', '37')
    EHIME = ('愛媛県', '38')
    KOCHI = ('高知県', '39')
    FUKUOKA = ('福岡県', '40')
    SAGA = ('佐賀県', '41')
    NAGASAKI = ('長崎県', '42')
    KUMAMOTO = ('熊本県', '43')
    OITA = ('大分県', '44')
    MIYAZAKI = ('宮崎県', '45')
    KAGOSHIMA = ('鹿児島県', '46')
    OKINAWA = ('沖縄県', '47')

    def __init__(self, ja: str, code: str):
        assert isinstance(code, str) and len(code) == 2, "都道府県コードは2桁です。"
        self.ja: str = ja
        self.code: str = code

    @staticmethod
    def value_of(name: str) -> Prefecture:
        for p in Prefecture:
            if p.ja == name:
                return p
        raise ValueError(f"{name} not found")


@dataclass(init=False, unsafe_hash=True, frozen=True)
class Address:
    """住所"""
    country: Literal['JP']
    postal_code: str | None
    prefecture: Prefecture
    city: str
    street: str

    def __init__(self, country: str, postal_code: str | None, prefecture: Prefecture, city: str, street: str):
        if postal_code is not None:
            assert isinstance(postal_code, str) and len(str(postal_code)) == 7, \
                f"郵便番号に{type(postal_code)}型の{postal_code}が指定されました。郵便番号には7桁の数字を入力してください。"
        super().__setattr__("country", country)
        super().__setattr__("postal_code", postal_code)
        super().__setattr__("prefecture", prefecture)
        super().__setattr__("city", city)
        super().__setattr__("street", street)

    @staticmethod
    def from_postal_code(postal_code: int) -> Address:
        """郵便番号指定で住所を取得できる"""
        pass

    def street(self, street: str) -> Address:
        """番地を入力できる"""
        return Address(self.country, self.postal_code, self.prefecture, self.city, street)
