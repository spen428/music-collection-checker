from checker import *


def _confirm(prompt: str) -> bool:
    yn = input(prompt) or 'y'
    if yn.lower() == 'n':
        return False
    if yn.lower() == 'y':
        return True

    print("Please answer [Y]es or [N]o.")
    return _confirm(prompt)


def _check(checker: BaseChecker):
    checker.check()

    print("========================================")
    print(f"{checker.name}:")
    print("========================================")

    count = 0
    for item in checker.issues():
        print(item)
        count += 1

    print("========================================")
    print(f"{count} issues in total")
    print("========================================")
    print("")


def run_all_checks(work_dir: str, confirm_before_each: bool):
    print("Checking music collection for issues...")

    walk = list(os.walk(work_dir))

    checkers: List[BaseChecker] = [
        EmptyDirChecker(work_dir, walk),
        MissingCoverArtChecker(work_dir, walk),
        BadDirNameChecker(work_dir, walk),
        UndesirableFileTypeChecker(work_dir, walk),
        MixedFileTypeChecker(work_dir, walk),
        BadFileNameChecker(work_dir, walk),
    ]

    for checker in checkers:
        if not confirm_before_each or _confirm(f"Execute '{checker.name}' check? [Yn]"):
            _check(checker)

    print("Done")
    print("Please review and action any issues listed above.")
