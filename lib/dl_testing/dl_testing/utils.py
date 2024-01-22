from __future__ import annotations

from contextlib import contextmanager
import http.client
import logging
import os
import socket
import time
from typing import (
    Any,
    Callable,
    List,
    Literal,
    Tuple,
    overload,
)

import pytest

from dl_api_commons.reporting.profiler import (
    PROFILING_LOG_NAME,
    QUERY_PROFILING_ENTRY,
)
from dl_testing.containers import get_test_container_hostport
from dl_testing.shared_testing_constants import RUN_DEVHOST_TESTS
from dl_utils.wait import wait_for


LOGGER = logging.getLogger(__name__)


def skip_outside_devhost(func):  # type: ignore  # 2024-01-22 # TODO: Function is missing a type annotation  [no-untyped-def]
    """
    Not all tests can run in just any environment (particularly in autotests).
    So put those under an environment flag.
    """
    if RUN_DEVHOST_TESTS:
        return func
    return pytest.mark.skip("Requires RUN_DEVHOST_TESTS=1")(func)


def wait_for_initdb(initdb_port, initdb_host=None, timeout=900, require: bool = False):  # type: ignore  # 2024-01-22 # TODO: Function is missing a return type annotation  [no-untyped-def]
    initdb_host = initdb_host or get_test_container_hostport("init-db").host
    # TODO: initdb_port?

    def check_initdb_liveness() -> Tuple[bool, Any]:
        try:
            conn = http.client.HTTPConnection(initdb_host, initdb_port)
            conn.request("GET", "/")
            resp = conn.getresponse()
            body = resp.read().decode("utf-8", errors="replace")
            if resp.status != 200:
                raise Exception("Non-ok response", dict(res=resp, status=resp.status, body=body))
            return True, body
        except Exception as exc:
            return False, dict(exc=exc)

    return wait_for(
        name="initdb readiness",
        condition=check_initdb_liveness,
        timeout=timeout,
        require=require,
    )


def wait_for_port(host: str, port: int, period_seconds: int = 1, timeout_seconds: int = 10):  # type: ignore  # 2024-01-22 # TODO: Function is missing a return type annotation  [no-untyped-def]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    time_start = time.time()

    while time.time() - time_start < timeout_seconds:
        try:
            sock.connect((host, port))
            sock.close()
            LOGGER.info(f"{host}:{port} is available")
            return
        except socket.error:
            LOGGER.warning(f"Waiting for {host}:{port} to become available")
            time.sleep(period_seconds)

    raise Exception(f"Timeout waiting for {host}:{port} to become available")


@overload
def get_log_record(  # type: ignore  # 2024-01-22 # TODO: Overloaded function signatures 1 and 2 overlap with incompatible return types  [misc]
    caplog: Any, predicate: Callable[[logging.LogRecord], bool], single: Literal[True] = True
) -> logging.LogRecord:
    pass


@overload
def get_log_record(
    caplog: Any, predicate: Callable[[logging.LogRecord], bool], single: Literal[False] = False
) -> List[logging.LogRecord]:
    pass


def get_log_record(caplog, predicate, single=False):  # type: ignore  # 2024-01-22 # TODO: Function is missing a type annotation  [no-untyped-def]
    log_records = [rec for rec in caplog.records if predicate(rec)]

    if single:
        assert len(log_records) == 1, f"Unexpected count of record in logs: {len(log_records)}"
        return log_records[0]

    return log_records


def guids_from_titles(result_schema: List[dict], titles: List[str]) -> List[str]:
    fields = [f["field"] if "field" in f else f for f in result_schema]
    guid_by_title = {f["title"]: f["guid"] for f in fields if f.get("title") in titles and f.get("guid")}
    return [guid_by_title[title] for title in titles]


@contextmanager
def override_env_cm(to_set: dict[str, str], purge: bool = False):  # type: ignore  # 2024-01-22 # TODO: Function is missing a return type annotation  [no-untyped-def]
    preserved = {k: v for k, v in os.environ.items()}

    try:
        if purge:
            for k in os.environ:
                del os.environ[k]
        for k, v in to_set.items():
            os.environ[k] = v
        yield
    finally:
        for k in to_set:
            del os.environ[k]
            # os.unsetenv(k)

        for k, v in preserved.items():
            os.environ[k] = v


def _is_profiling_record(rec) -> bool:  # type: ignore  # 2024-01-22 # TODO: Function is missing a type annotation for one or more arguments  [no-untyped-def]
    return rec.name == PROFILING_LOG_NAME and rec.msg == QUERY_PROFILING_ENTRY


def get_dump_request_profile_records(caplog, single: bool = False):  # type: ignore  # 2024-01-22 # TODO: Function is missing a return type annotation  [no-untyped-def]
    return get_log_record(  # type: ignore  # 2024-01-22 # TODO: No overload variant of "get_log_record" matches argument types "Any", "Callable[[Any], bool]", "bool"  [call-overload]
        caplog,
        predicate=_is_profiling_record,
        single=single,
    )
