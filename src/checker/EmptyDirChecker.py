from checker import BaseChecker


class EmptyDirChecker(BaseChecker):
    def __init__(self, work_dir: str):
        super().__init__('Empty directories', work_dir)

    def _check(self, current_path: str, dirs: list, files: list, depth: int):
        if len(dirs) == 0 and len(files) == 0:
            self._log_issue(current_path + '/')
