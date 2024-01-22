from dl_formula.connectors.base.column import UnprefixedColumnRenderer
from dl_formula.connectors.base.connector import FormulaConnector
from dl_sqlalchemy_metrica_api.base import MetrikaApiDialect as SAMetrikaApiDialect  # type: ignore  # 2024-01-22 # TODO: Skipping analyzing "dl_sqlalchemy_metrica_api.base": module is installed, but missing library stubs or py.typed marker  [import]

from dl_connector_metrica.formula.constants import MetricaDialect as MetricaDialectNS
from dl_connector_metrica.formula.definitions.all import DEFINITIONS


class MetricaFormulaConnector(FormulaConnector):
    dialect_ns_cls = MetricaDialectNS
    dialects = MetricaDialectNS.METRIKAAPI
    default_dialect = MetricaDialectNS.METRIKAAPI
    op_definitions = DEFINITIONS
    sa_dialect = SAMetrikaApiDialect()
    column_renderer_cls = UnprefixedColumnRenderer
