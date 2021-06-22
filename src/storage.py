import os
from copy import deepcopy
from typing import List, Optional


class Storage:

    def __init__(self, filename: str) -> None:
        self._cache: Optional[List[str]] = None
        self._filename = filename

        if not os.path.exists(self._filename):
            with open(self._filename, 'w'):
                pass

        with open(self._filename) as f:
            self._cache = [r.strip() for r in f.readlines() if r.strip()]
        print('[Storage] loaded %d' % len(self._cache))

    def get_all(self) -> List[str]:
        return deepcopy(self._cache)

    def is_saved(self, row: str) -> bool:
        return row in self._cache

    def add(self, row: str) -> None:
        if row not in self._cache:
            self._cache.append(row)

        with open(self._filename, 'w') as f:
            f.write('\n'.join(self._cache))


if __name__ == '__main__':
    def f7(seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]

    s = Storage('haty.txt')
    print(len(s._cache), len(set(s._cache)))

    # with open('haty.txt', 'w') as f:
    #     f.write('\n'.join(f7(s._cache)))
