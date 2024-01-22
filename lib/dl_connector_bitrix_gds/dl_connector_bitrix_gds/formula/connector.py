from dl_formula.connectors.base.connector import FormulaConnector
from dl_sqlalchemy_bitrix.base import BitrixDialect as SABitrixDialect  # type: ignore  # 2024-01-22 # TODO: Skipping analyzing "dl_sqlalchemy_bitrix.base": module is installed, but missing library stubs or py.typed marker  [import]

from dl_connector_bitrix_gds.formula.constants import BitrixDialect as BitrixDialectNS
from dl_connector_bitrix_gds.formula.definitions.all import DEFINITIONS


class BitrixGDSFormulaConnector(FormulaConnector):
    dialect_ns_cls = BitrixDialectNS
    dialects = BitrixDialectNS.BITRIX
    default_dialect = BitrixDialectNS.BITRIX
    op_definitions = DEFINITIONS
    sa_dialect = SABitrixDialect()
