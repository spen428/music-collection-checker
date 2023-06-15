import os.path
import re
from typing import List

from . import BaseChecker, WalkItem


class BadDirNameChecker(BaseChecker):
    _min_depth: int

    def __init__(self, work_dir: str, walk: List[WalkItem], ignore_dirs_with_depth_less_than: int = 0):
        super().__init__('Bad directory names', work_dir, walk)
        self._min_depth = ignore_dirs_with_depth_less_than

    regex = re.compile(r"^\[\d{4}-\d{2}-\d{2}] .+$")

    def _check(self, current_path: str, dirs: list, files: list, depth: int):
        if depth < self._min_depth:
            return
        basename = os.path.basename(current_path)
        if not self.regex.match(basename):
            self._log_issue(current_path + '/')
