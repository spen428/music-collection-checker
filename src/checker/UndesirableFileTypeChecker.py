import re
from typing import List

from . import BaseChecker, WalkItem


class UndesirableFileTypeChecker(BaseChecker):
    def __init__(self, work_dir: str, walk: List[WalkItem]):
        super().__init__('Undesirable file types', work_dir, walk)

    regex = re.compile(r".+\.(mp3|ogg|flac|ptsp|jpg|png)")

    def _check(self, current_path: str, dirs: list, files: list, depth: int):
        if len(files) == 0:
            return

        undesirable_files = [filename for filename in files if not self.regex.match(filename)]
        for filename in undesirable_files:
            self._log_issue(current_path + '/' + filename)
