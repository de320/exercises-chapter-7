from numbers import Integral  # noqa F401


class VerifiedSet(set):
    def __init__(self, iterable=()):
        super().__init__()
        for item in iterable:
            self.add(item)

    def _verify(self, item):
        raise NotImplementedError

    def add(self, item):
        self._verify(item)
        super().add(item)

    def update(self, *args):
        for iterable in args:
            for item in iterable:
                self._verify(item)
                super().add(item)

    def symmetric_difference_update(self, other):
        for item in other:
            self._verify(item)
        super().symmetric_difference_update(other)

    # Redefine methods that create new sets
    def union(self, *args):
        new_set = self.__class__()
        for s in (self, *args):
            for item in s:
                new_set.add(item)
        return new_set

    def intersection(self, *args):
        new_set = self.__class__()
        for other_set in args:
            for item in other_set:
                self._verify(item)  # Verify each item
        for item in super().intersection(*args):
            new_set.add(item)
        return new_set

    def difference(self, *args):
        new_set = self.__class__()
        for other_set in args:
            for item in other_set:
                self._verify(item)  # Verify each item
        for item in super().difference(*args):
            new_set.add(item)
        return new_set

    def symmetric_difference(self, other):
        new_set = self.__class__()
        for item in super().symmetric_difference(other):
            new_set.add(item)
        return new_set

    def copy(self):
        new_set = self.__class__()
        for item in self:
            new_set.add(item)
        return new_set


class IntSet(VerifiedSet):
    def _verify(self, item):
        if not isinstance(item, Integral):
            raise TypeError(
                f"IntSet expected an integer, got a {type(item).__name__}.")


class UniquenessError(KeyError):
    """Raised when a duplicate value is added to a UniqueSet."""


class UniqueSet(VerifiedSet):
    def _verify(self, item):
        if item in self:
            raise UniquenessError(
                f"Duplicate value '{item}' not allowed in UniqueSet.")
