import re
from typing import List

from . import BaseChecker, WalkItem


class BadFileNameChecker(BaseChecker):
    def __init__(self, work_dir: str, walk: List[WalkItem]):
        super().__init__('Bad file names', work_dir, walk)

    track_regex = re.compile(r"^(\d{2}-)?\d{2}\. .+\.[a-z0-9]{3,4}$")
    cover_regex = re.compile(r"^cover\.(jpg|png)$")

    def _check(self, current_path: str, dirs: list, files: list, depth: int):
        if depth < 3:
            return
        for filename in files:
            if self.track_regex.match(filename):
                continue
            if self.cover_regex.match(filename):
                continue
            self._log_issue(current_path + '/' + filename)
