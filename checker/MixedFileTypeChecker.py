import os.path
from typing import Set

from checker.BaseChecker import BaseChecker


class MixedFileTypeChecker(BaseChecker):
    file_extensions: Set[str] = set()

    def __init__(self, work_dir: str):
        super().__init__('Mixed file types', work_dir)

    def _check(self, current_path: str, dirs: list, files: list):
        if len(files) == 0:
            return

        file_extensions = set([os.path.splitext(f)[-1] for f in files])
        if len(file_extensions) > 2:
            self._log_error(f"{current_path}/  ({','.join(file_extensions)})")
