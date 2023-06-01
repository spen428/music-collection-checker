from checker.BaseChecker import BaseChecker


class EmptyDirChecker(BaseChecker):
    def __init__(self, work_dir: str):
        super().__init__('Empty directories', work_dir)

    def _check(self, current_path: str, dirs: list, files: list):
        if len(dirs) == 0 and len(files) == 0:
            self._log_error(current_path + '/')
