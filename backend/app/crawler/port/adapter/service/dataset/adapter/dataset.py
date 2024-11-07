import re
from typing import override

from crawler.domain.model.interim import Interim
from crawler.port.adapter.service.dataset.adapter import DatasetAdapter
from dataset.application.company.command import SaveCompanyCommand
from dataset.port.adapter.resource.company import CompanyResource


class DatasetModuleAdapter(DatasetAdapter):
    def __init__(self):
        self.__company_resource = CompanyResource()
        self.__location_pattern = '''(...??[都道府県])((?:旭川|伊達|石狩|盛岡|奥州|田村|南相馬|那須塩原|東村山|武蔵村山|羽村|十日町|上越|
富山|野々市|大町|蒲郡|四日市|姫路|大和郡山|廿日市|下松|岩国|田川|大村|宮古|富良野|別府|佐伯|黒部|小諸|塩尻|玉野|
周南)市|(?:余市|高市|[^市]{2,3}?)郡(?:玉村|大町|.{1,5}?)[町村]|(?:.{1,4}市)?[^町]{1,4}?区|.{1,7}?[市町村])(.+)'''

    @override
    def transfer(self, dataset_name: str, interim: Interim) -> None:
        result = re.match(self.__location_pattern, interim.get('location'))
        if not result:
            return

        prefecture = result.group(1)
        city = result.group(2)
        street = result.group(3)

        command = SaveCompanyCommand(
            uuid=None,
            corporate_number=interim.get('corporate_number'),
            name=interim.get('name'),
            description=interim.get('business_summary'),
            founded_at=interim.get('date_of_establishment'),
            homepage=interim.get('company_url'),
            same_as=list(filter(lambda x: x is not None, [
                interim.get('company_url')
            ])),
            summaries={
                'representative': interim.get('representative_name'),
                'capital': interim.get('capital_stock'),
                # 'sales': '売上高',
                'employees': interim.get('employee_number')
            },
            contact_points=[],
            offices=[
                SaveCompanyCommand.Address(
                    country='JP',
                    postal_code=interim.get('postal_code'),
                    prefecture=prefecture,
                    city=city,
                    street=street
                )
            ]
        )
        self.__company_resource.company_application_service.save(command)
