from injector import singleton, inject

from crawler.domain.model.interim import InterimId, Interim
from crawler.port.adapter.persistence.repository.mysql.interim import DriverManagerInterim


@singleton
class CacheLayerInterim:
    """キャッシュを保持するクラス"""
    values = dict()

    # 60秒 × 15分
    __TTL = 60 * 15

    @inject
    def __init__(self, driver_manager_interim: DriverManagerInterim):
        self.__driver_manager_interim = driver_manager_interim

    def cache_or_origin(self, id: InterimId) -> Interim | None:
        optional = self.__driver_manager_interim.find_by_id(id)
        if optional is None:
            return None
        return optional

    def caches_or_origins(self, *id: InterimId) -> set[Interim]:
        return self.__driver_manager_interim.find_by_ids(*id)
        pass

    def set(self, interim: Interim) -> None:
        self.__driver_manager_interim.upsert(interim)
        # キャッシュを更新する
        # self.values[f'uuid-{company.id.type_of(CompanyId.Type.UUID).value}'] = company
        # self.values[f'jcn-{company.id.type_of(CompanyId.Type.JCN).value}'] = company

    def delete(self, interim: Interim) -> None:
        self.__driver_manager_interim.delete(interim)
        # # キャッシュを更新する
        # self.values[f'email_address-{user.email_address.text}'] = None
