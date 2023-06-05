#!/usr/bin/env python3
import os

import runner

if __name__ == '__main__':
    music_dir = os.path.join(os.path.expanduser("~"), "Music")
    runner.run_all_checks(music_dir, confirm_before_each=True)
