from clickhouse_sqlalchemy.drivers.base import ClickHouseDialect as SAClickHouseDialect  # type: ignore  # 2024-01-22 # TODO: Skipping analyzing "clickhouse_sqlalchemy.drivers.base": module is installed, but missing library stubs or py.typed marker  [import]

from dl_formula.connectors.base.connector import FormulaConnector

from dl_connector_clickhouse.formula.constants import ClickHouseDialect as ClickHouseDialectNS
from dl_connector_clickhouse.formula.definitions.all import DEFINITIONS
from dl_connector_clickhouse.formula.literal import ClickHouseLiteralizer
from dl_connector_clickhouse.formula.type_constructor import ClickHouseTypeConstructor


class ClickHouseFormulaConnector(FormulaConnector):
    dialect_ns_cls = ClickHouseDialectNS
    dialects = ClickHouseDialectNS.CLICKHOUSE
    default_dialect = ClickHouseDialectNS.CLICKHOUSE_21_8
    op_definitions = DEFINITIONS
    literalizer_cls = ClickHouseLiteralizer
    type_constructor_cls = ClickHouseTypeConstructor
    sa_dialect = SAClickHouseDialect()
