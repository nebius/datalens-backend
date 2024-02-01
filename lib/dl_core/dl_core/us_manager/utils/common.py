from __future__ import annotations

import collections
from typing import Type


def inheritors(klass: Type):  # type: ignore  # 2024-02-01 # TODO: Function is missing a return type annotation  [no-untyped-def]
    subclasses = set()
    work = collections.deque([klass])
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                work.append(child)
    return subclasses
