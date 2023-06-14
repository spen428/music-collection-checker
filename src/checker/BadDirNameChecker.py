import os.path
import re
from typing import List

from . import BaseChecker, WalkItem


class BadDirNameChecker(BaseChecker):
    def __init__(self, work_dir: str, walk: List[WalkItem]):
        super().__init__('Bad directory names', work_dir, walk)

    regex = re.compile(r"^\[\d{4}-\d{2}-\d{2}] .+$")

    def _check(self, current_path: str, dirs: list, files: list, depth: int):
        if depth < 3:
            return
        basename = os.path.basename(current_path)
        if not self.regex.match(basename):
            self._log_issue(current_path + '/')
