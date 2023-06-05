import os
from typing import List, Iterator


class BaseChecker(object):
    name: str
    _issues: List[str]

    def __init__(self, name: str, work_dir: str):
        self.name = name
        self.work_dir = work_dir
        self.work_dir_len: int = len(work_dir)
        self._issues = []

    def _log_issue(self, file_path: str):
        num_chars_to_skip = self.work_dir_len + 1
        self._issues.append(file_path[num_chars_to_skip:])

    def issues(self) -> Iterator[str]:
        return iter(self._issues)

    def check(self):
        self._pre_check()
        for current_path, dirs, files in os.walk(self.work_dir):
            if self._should_skip(current_path, dirs, files):
                continue
            depth = len(current_path[self.work_dir_len:].split('/'))
            self._check(current_path, dirs, files, depth)
        self._post_check()

    def _pre_check(self):
        pass

    def _check(self, current_path: str, dirs: list, files: list, depth: int):
        raise NotImplementedError

    def _post_check(self):
        pass

    def _should_skip(self, current_path: str, dirs: list, files: list) -> bool:
        return current_path.startswith(self.work_dir + '/Unsorted Music') \
            or current_path.startswith(self.work_dir + '/.config')
