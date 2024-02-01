# coding: utf-8
from __future__ import annotations

from collections import defaultdict
import contextvars
import sys

import six


_LOG_CONTEXT = contextvars.ContextVar("_LOG_CONTEXT", default=None)


def force_unicode(obj):  # type: ignore  # 2024-02-01 # TODO: Function is missing a type annotation  [no-untyped-def]
    if not isinstance(obj, six.string_types):
        obj = repr(obj)
    return obj.decode(sys.getdefaultencoding())


class ContextFormatter:
    @classmethod
    def is_context_exist(cls):  # type: ignore  # 2024-02-01 # TODO: Function is missing a return type annotation  [no-untyped-def]
        return _LOG_CONTEXT.get() is not None

    @classmethod
    def get_or_create_logging_context(cls):  # type: ignore  # 2024-02-01 # TODO: Function is missing a return type annotation  [no-untyped-def]
        if not cls.is_context_exist():
            _LOG_CONTEXT.set(defaultdict(list))  # type: ignore  # 2024-02-01 # TODO: Argument 1 to "set" of "ContextVar" has incompatible type "defaultdict[<nothing>, list[_T]]"; expected "None"  [arg-type]
        return _LOG_CONTEXT.get()


def reset_context():  # type: ignore  # 2024-02-01 # TODO: Function is missing a return type annotation  [no-untyped-def]
    _LOG_CONTEXT.set(defaultdict(list))  # type: ignore  # 2024-02-01 # TODO: Argument 1 to "set" of "ContextVar" has incompatible type "defaultdict[<nothing>, list[_T]]"; expected "None"  [arg-type]


def put_to_context(key, value):  # type: ignore  # 2024-02-01 # TODO: Function is missing a type annotation  [no-untyped-def]
    ctx = ContextFormatter.get_or_create_logging_context()
    ctx[key].append(value)


def pop_from_context(key):  # type: ignore  # 2024-02-01 # TODO: Function is missing a type annotation  [no-untyped-def]
    if not ContextFormatter.is_context_exist():
        return
    ctx = ContextFormatter.get_or_create_logging_context()
    if key not in ctx:
        return
    value = ctx[key].pop()
    if not ctx[key]:
        del ctx[key]
    return value


class LogContext(object):
    context = None

    def __init__(self, **context):  # type: ignore  # 2024-02-01 # TODO: Function is missing a type annotation  [no-untyped-def]
        self.context = context

    def __enter__(self):  # type: ignore  # 2024-02-01 # TODO: Function is missing a type annotation  [no-untyped-def]
        for key, value in self.context.items():  # type: ignore  # 2024-02-01 # TODO: Item "None" of "dict[str, Any] | None" has no attribute "items"  [union-attr]
            put_to_context(key, value)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):  # type: ignore  # 2024-02-01 # TODO: Function is missing a type annotation  [no-untyped-def]
        for key in self.context:  # type: ignore  # 2024-02-01 # TODO: Item "None" of "dict[str, Any] | None" has no attribute "__iter__" (not iterable)  [union-attr]
            pop_from_context(key)
        return False


log_context = LogContext


def get_log_context():  # type: ignore  # 2024-02-01 # TODO: Function is missing a return type annotation  [no-untyped-def]
    if not ContextFormatter.is_context_exist():
        return {}
    ctx = ContextFormatter.get_or_create_logging_context()
    return {key: values[-1] for key, values in ctx.items()}
