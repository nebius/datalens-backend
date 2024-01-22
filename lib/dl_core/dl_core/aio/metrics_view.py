from __future__ import annotations

import os
from typing import ClassVar

from aiohttp import web
from statcommons.unistat.common import dump_for_prometheus  # type: ignore  # 2024-01-22 # TODO: Skipping analyzing "statcommons.unistat.common": module is installed, but missing library stubs or py.typed marker  [import]
from statcommons.unistat.uwsgi import uwsgi_prometheus  # type: ignore  # 2024-01-22 # TODO: Skipping analyzing "statcommons.unistat.uwsgi": module is installed, but missing library stubs or py.typed marker  [import]

from dl_api_commons.aiohttp.aiohttp_wrappers import (
    DLRequestView,
    RequiredResource,
    RequiredResourceCommon,
)


class MetricsView(DLRequestView):
    REQUIRED_RESOURCES: ClassVar[frozenset[RequiredResource]] = frozenset({RequiredResourceCommon.SKIP_AUTH})

    async def get(self) -> web.Response:
        result = []
        if os.environ.get("UWSGI_STATS"):
            uwsgi_metrics = uwsgi_prometheus(label_prefix="uwsgi_")
            result.extend(uwsgi_metrics)

        body = "".join(dump_for_prometheus(result))
        return web.Response(text=body)
