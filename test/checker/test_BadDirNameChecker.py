from pprint import pprint
from unittest import TestCase

from parameterized import parameterized

from StringToFilesystem import string_to_filesystem
from checker import BadDirNameChecker


class TestBadDirNameChecker(TestCase):
    @parameterized.expand([
        ('[2002-02-02] Title', True),
        ('[2002-02-02] Album Title', True),
        ('[2002-2-02] Album Title', False),
        ('[2002-02-2] Album Title', False),
        ('Directory', False),
        ('[2002] Directory', False),
        ('[2002-02] Directory', False),
        ('[2002-02-02] ', False),
        ('[2002-02-02]', False),
    ])
    def test__check_basic_valid_and_invalid_dir_names(self, dirname: str, is_valid: bool):
        sut = BadDirNameChecker('/mnt/music/Metal', string_to_filesystem(f'/mnt/music/Metal/{dirname}/Track 1.ogg'))
        sut.check()

        issues = [x for x in sut.issues()]
        if is_valid:
            self.assertNotIn(dirname, issues)
        else:
            self.assertIn(dirname, issues)

    def test__check_with_min_depth_parameter(self):
        filesystem = '''
/mnt/music/Unsorted/
/mnt/music/Metal/Unsorted/
/mnt/music/Metal/[1999-01-01] Album Title/Track 1.ogg
/mnt/music/Metal/Heavy/[1999-01-01] Album Title/Track 1.ogg
        '''
        to_filesystem = string_to_filesystem(filesystem)
        pprint(to_filesystem)
        sut = BadDirNameChecker('/mnt/music', to_filesystem, ignore_dirs_with_depth_less_than=3)
        sut.check()

        issues = [x for x in sut.issues()]
        self.assertIn('Metal/Unsorted', issues)
        self.assertIn('Metal/Heavy', issues)
