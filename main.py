#!/usr/bin/env python3
import os
from typing import List

from checker import BaseChecker, EmptyDirChecker, MissingCoverArtChecker, BadDirNameChecker, UndesirableFileTypeChecker, \
    MixedFileTypeChecker, BadFileNameChecker


def check(checker: BaseChecker):
    # yn = input(f"Execute '{checker.name}' check? [Yn]") or 'y'
    # if yn.lower() == 'n':
    #     return
    # if yn.lower() != 'y':
    #     print("Please answer [Y]es or [N]o.")
    #     check(checker)
    #     return

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


def run(work_dir: str):
    checkers: List[BaseChecker] = [
        EmptyDirChecker(work_dir),
        MissingCoverArtChecker(work_dir),
        BadDirNameChecker(work_dir),
        UndesirableFileTypeChecker(work_dir),
        MixedFileTypeChecker(work_dir),
        BadFileNameChecker(work_dir)
    ]

    print("Checking music collection for issues...")

    for checker in checkers:
        check(checker)

    print("Done")
    print("Please review and action any issues listed above.")


if __name__ == '__main__':
    music_dir = os.path.join(os.path.expanduser("~"), "Music")
    run(music_dir)
