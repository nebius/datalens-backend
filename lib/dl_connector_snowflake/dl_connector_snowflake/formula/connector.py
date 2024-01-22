from snowflake.sqlalchemy.snowdialect import SnowflakeDialect as SASnowflakeDialect  # type: ignore  # 2024-01-22 # TODO: Skipping analyzing "snowflake.sqlalchemy.snowdialect": module is installed, but missing library stubs or py.typed marker  [import]

from dl_formula.connectors.base.connector import FormulaConnector

from dl_connector_snowflake.formula.constants import SnowFlakeDialect as SnowFlakeDialectNS
from dl_connector_snowflake.formula.definitions.all import DEFINITIONS
from dl_connector_snowflake.formula.literal import SnowFlakeLiteralizer


class SnowFlakeFormulaConnector(FormulaConnector):
    dialect_ns_cls = SnowFlakeDialectNS
    dialects = SnowFlakeDialectNS.SNOWFLAKE
    default_dialect = SnowFlakeDialectNS.SNOWFLAKE
    op_definitions = DEFINITIONS
    literalizer_cls = SnowFlakeLiteralizer
    sa_dialect = SASnowflakeDialect()
