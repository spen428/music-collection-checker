import re
from typing import List

from . import BaseChecker, WalkItem


class MissingCoverArtChecker(BaseChecker):
    def __init__(self, work_dir: str, walk: List[WalkItem]):
        super().__init__('Missing cover art', work_dir, walk)

    regex = re.compile(r"cover\.(jpg|png)")

    def _check(self, current_path: str, dirs: list, files: list, depth: int):
        if len(files) == 0:
            return

        cover_art_files = [self.regex.match(filename) for filename in files]
        if not any(cover_art_files):
            self._log_issue(current_path + '/')
