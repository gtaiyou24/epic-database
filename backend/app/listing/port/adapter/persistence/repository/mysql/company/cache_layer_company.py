from injector import singleton, inject

from listing.domain.model.company import Company, CompanyId
from listing.port.adapter.persistence.repository.mysql.company import DriverManagerCompany


@singleton
class CacheLayerCompany:
    """キャッシュを保持するクラス"""
    values = dict()

    # 60秒 × 15分
    __TTL = 60 * 15

    @inject
    def __init__(self, driver_manager_company: DriverManagerCompany):
        self.__driver_manager_company = driver_manager_company

    def cache_or_origin(self, company_id: CompanyId) -> Company | None:
        uuid = company_id.type_of(CompanyId.Type.UUID)
        if uuid and f'uuid-{uuid.value}' in self.values.keys():
            return self.values[f'uuid-{uuid.value}']

        jcn = company_id.type_of(CompanyId.Type.JCN)
        if jcn and f'jcn-{jcn.value}' in self.values.keys():
            return self.values[f'jcn-{jcn.value}']

        optional = self.__driver_manager_company.find_by_id(company_id)
        if optional is None:
            return None
        self.values[f'uuid-{optional.id.type_of(CompanyId.Type.UUID).value}'] = optional
        self.values[f'jcn-{optional.id.type_of(CompanyId.Type.JCN).value}'] = optional
        return optional

    def caches_or_origins(self, *company_id: CompanyId) -> set[Company] | None:
        # return self.__driver_manager_user.find_by_ids(*company_id)
        pass

    def set(self, company: Company) -> None:
        self.__driver_manager_company.upsert(company)
        print(company.id)
        # キャッシュを更新する
        self.values[f'uuid-{company.id.type_of(CompanyId.Type.UUID).value}'] = company
        self.values[f'jcn-{company.id.type_of(CompanyId.Type.JCN).value}'] = company

    def delete(self, company: Company) -> None:
        # self.__driver_manager_user.delete(user)
        # # キャッシュを更新する
        # self.values[f'email_address-{user.email_address.text}'] = None
        pass
