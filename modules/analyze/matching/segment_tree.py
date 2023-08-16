class RangeUpdatePointQuery:
    """
    Here, idx will be 0 ~ n - 1. so need modif in this class.
    """

    def __init__(self, n):
        self.nodes = n + 1
        self.tree = [0] * (n + 1)

    def _update(self, i, v):
        while i < self.nodes:
            self.tree[i] += v
            i += i & -i

    def _get(self, i):
        res = 0
        while i:
            res += self.tree[i]
            i -= i & -i
        return res

    def update(self, i, j, v):
        self._update(i + 1, v)
        self._update(j + 2, -v)

    def get(self, i):
        return self._get(i + 1)
