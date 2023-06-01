import os.path
import re

from checker.BaseChecker import BaseChecker


class BadDirNameChecker(BaseChecker):
    def __init__(self, work_dir: str):
        super().__init__('Bad directory names', work_dir)

    regex = re.compile(r"^\[\d{4}-\d{2}-\d{2}] .+$")

    def _check(self, current_path: str, dirs: list, files: list):
        depth = len(current_path[self.work_dir_len:].split('/'))
        if depth < 3:
            return
        basename = os.path.basename(current_path)
        if not self.regex.match(basename):
            self._log_error(current_path + '/')
