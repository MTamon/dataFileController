"""Implement Basic Filter Class"""

from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import List


class Filter(metaclass=ABCMeta):
    """Basic Filter Class"""

    @abstractmethod
    def __call__(self, target: object) -> bool:
        raise NotImplementedError()

    @staticmethod
    def tile(filters: List[Filter] | Filter) -> TiledFilter:
        """Generate TiledFilter instance with `filters`.

        Args:
            filters (List[Filter] | Filter)

        Returns:
            TiledFilter: Compound filter consisting of a fFilter joined by the OR operator.
        """

        if isinstance(filters, Filter):
            filters = [Filter]
        elif not isinstance(filters, list):
            raise TypeError(
                f"The argument 'filters' type must be 'Filter' or 'List[Filter]', \
                    but detect '{type(filters)}'"
            )
        elif filters == []:
            return TiledFilter(None)
        elif not isinstance(filters[0], Filter):
            raise TypeError(
                f"The argument 'filters' type must be 'Filter' or 'List[Filter]', \
                    but detect '{type(filters)}'"
            )
        return TiledFilter(filters)

    @staticmethod
    def overlap(filters: List[Filter] | Filter) -> OverlapedFilter:
        """Generate OverlapedFilter instance with `filters`.

        Args:
            filters (List[Filter] | Filter)

        Returns:
            OverlapedFilter: Compound filter consisting of a fFilter joined by the AND operator.
        """

        if isinstance(filters, Filter):
            filters = [Filter]
        elif not isinstance(filters, list):
            raise TypeError(
                f"The argument 'filters' type must be 'Filter' or 'List[Filter]', \
                    but detect '{type(filters)}'"
            )
        elif filters == []:
            return OverlapedFilter(None)
        elif not isinstance(filters[0], Filter):
            raise TypeError(
                f"The argument 'filters' type must be 'Filter' or 'List[Filter]', \
                    but detect '{type(filters)}'"
            )
        return OverlapedFilter(filters)


class TiledFilter(Filter):
    """Compound filter consisting of a fFilter joined by the OR operator."""

    def __init__(self, filters: List[Filter]) -> None:
        super().__init__()
        self.filters = filters

    def __call__(self, target: object) -> bool:
        for _f in self.filters:
            if _f(target=target):
                return True
        return False


class OverlapedFilter(Filter):
    """Compound filter consisting of a fFilter joined by the AND operator."""

    def __init__(self, filters: List[Filter]) -> None:
        super().__init__()
        self.filters = filters

    def __call__(self, target: object) -> bool:
        for _f in self.filters:
            if not _f(target=target):
                return False
        return True


class EmpFilter(Filter):
    """Empty Filter"""

    def __call__(self, target: object) -> bool:
        return True
