import argparse
from enum import Enum


class Module(Enum):
    APIGATEWAY = 'api-gateway'
    # MARKET = ('market', lambda: MarketBatch())

#     def __init__(self, module_name: str, instance: Callable[[], ModuleBatch]):
#         self.module_name = module_name
#         self.batch = instance()
#
#     def run(self, name: str, *args) -> None:
#         self.batch.startup()
#         self.batch.run(name, *args)
#         self.batch.shutdown()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Batch')
    parser.add_argument("module", type=str, choices=[e.name for e in Module],
                        help="モジュール名を指定してください。")
    parser.add_argument("name", type=str, help="バッチ名を指定してください。")

    args = parser.parse_args()

    print("Module:", args.module)
    print("Name:", args.name)

    # Module[args.module].run(args.name, args.args)
