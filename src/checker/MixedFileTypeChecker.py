from typing import Set, List

from . import BaseChecker, WalkItem


class MixedFileTypeChecker(BaseChecker):
    file_extensions: Set[str] = set()

    def __init__(self, work_dir: str, walk: List[WalkItem]):
        super().__init__('Mixed file types', work_dir, walk)

    def _check(self, current_path: str, dirs: list, files: list, depth: int):
        if len(files) == 0:
            return

        file_extensions = set([filename.split('.')[-1] for filename in files])
        if len(file_extensions) > 2:
            self._log_issue(f"{current_path}/  ({','.join(file_extensions)})")
