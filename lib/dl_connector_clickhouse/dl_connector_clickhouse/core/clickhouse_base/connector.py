from clickhouse_sqlalchemy.orm.query import Query as CHQuery  # type: ignore  # 2024-01-22 # TODO: Skipping analyzing "clickhouse_sqlalchemy.orm.query": module is installed, but missing library stubs or py.typed marker  [import]

from dl_core.connectors.base.connector import (
    CoreBackendDefinition,
    CoreConnector,
)

from dl_connector_clickhouse.core.clickhouse_base.adapters import (
    AsyncClickHouseAdapter,
    ClickHouseAdapter,
)
from dl_connector_clickhouse.core.clickhouse_base.constants import BACKEND_TYPE_CLICKHOUSE
from dl_connector_clickhouse.core.clickhouse_base.query_compiler import ClickHouseQueryCompiler
from dl_connector_clickhouse.core.clickhouse_base.sa_types import SQLALCHEMY_CLICKHOUSE_TYPES


class ClickHouseCoreBackendDefinition(CoreBackendDefinition):
    backend_type = BACKEND_TYPE_CLICKHOUSE
    compiler_cls = ClickHouseQueryCompiler
    query_cls = CHQuery


class ClickHouseCoreConnectorBase(CoreConnector):
    backend_definition = ClickHouseCoreBackendDefinition
    rqe_adapter_classes = frozenset({ClickHouseAdapter, AsyncClickHouseAdapter})
    sa_types = SQLALCHEMY_CLICKHOUSE_TYPES
