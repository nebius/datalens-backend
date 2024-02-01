from __future__ import annotations

import flask


def _ping_handler():
    return ""


def _ping_handler_hax():
    if flask.request.method == "GET" and flask.request.path.rstrip("/") == "/ping":
        return _ping_handler()
    return None  # flask: fall through


def register_ping_handler_hax(app):
    # HAX to avoid bumping into inappropriate authorization added in 'before_request'.
    app.before_request(_ping_handler_hax)
