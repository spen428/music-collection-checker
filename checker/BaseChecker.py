import os
from typing import List, Iterator


class BaseChecker(object):
    name: str
    _items: List[str]

    def __init__(self, name: str, work_dir: str):
        self.name = name
        self.work_dir = work_dir
        self.work_dir_len: int = len(work_dir)
        self._items = []

    def _log_error(self, item: str):
        num_chars_to_skip = self.work_dir_len + 1
        self._items.append(item[num_chars_to_skip:])

    def issues(self) -> Iterator[str]:
        return iter(self._items)

    def check(self):
        self._pre_check()
        for current_path, dirs, files in os.walk(self.work_dir):
            depth = len(current_path[self.work_dir_len:].split('/'))
            self._check(current_path, dirs, files, depth)
        self._post_check()

    def _check(self, current_path: str, dirs: list, files: list, depth: int):
        raise NotImplementedError

    def _pre_check(self):
        pass

    def _post_check(self):
        pass
