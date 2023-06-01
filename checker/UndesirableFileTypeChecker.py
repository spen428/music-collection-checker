import re

from checker.BaseChecker import BaseChecker


class UndesirableFileTypeChecker(BaseChecker):
    def __init__(self, work_dir: str):
        super().__init__('Undesirable file types', work_dir)

    regex = re.compile(r".+\.(mp3|ogg|flac|ptsp|jpg|png)")

    def _check(self, current_path: str, dirs: list, files: list, depth: int):
        if len(files) == 0:
            return

        undesirable_files = [filename for filename in files if not self.regex.match(filename)]
        for filename in undesirable_files:
            self._log_error(current_path + '/' + filename)
