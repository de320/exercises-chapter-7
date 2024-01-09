import numpy as np
from example_code.groups import Group, Element  # noqa F401


class SymmetricGroup(Group):
    symbol = "S"

    def _validate(self, value):
        """Validate if the value is a valid permutation for the group."""
        if not isinstance(value, np.ndarray):
            raise ValueError("Group elements must be numpy arrays.")
        if len(value) != self.n or set(value) != set(range(self.n)):
            raise ValueError("Invalid permutation for the symmetric group.")

    def operation(self, a, b):
        """Perform the group operation: composition of permutations."""
        return a[b]
