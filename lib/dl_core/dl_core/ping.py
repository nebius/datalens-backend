from __future__ import annotations

import flask


def _ping_handler():  # type: ignore  # 2024-02-01 # TODO: Function is missing a return type annotation  [no-untyped-def]
    return ""


def _ping_handler_hax():  # type: ignore  # 2024-02-01 # TODO: Function is missing a return type annotation  [no-untyped-def]
    if flask.request.method == "GET" and flask.request.path.rstrip("/") == "/ping":
        return _ping_handler()
    return None  # flask: fall through


def register_ping_handler_hax(app):  # type: ignore  # 2024-02-01 # TODO: Function is missing a type annotation  [no-untyped-def]
    # HAX to avoid bumping into inappropriate authorization added in 'before_request'.
    app.before_request(_ping_handler_hax)
