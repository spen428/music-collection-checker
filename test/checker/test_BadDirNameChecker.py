from unittest import TestCase

from parameterized import parameterized

from StringToFilesystem import string_to_filesystem
from checker import BadDirNameChecker


class TestBadDirNameChecker(TestCase):
    filesystem = string_to_filesystem("""
/mnt/music/Metal/[2222-22-22] Dir/
/mnt/music/Metal/Dir/
/mnt/music/Metal/[2222] Dir/
/mnt/music/Metal/[2222-22] Dir/
/mnt/music/Metal/[2222-22-22] /
/mnt/music/Metal/[2222-22-22]/
    """)

    @parameterized.expand([
        ('Metal/[2222-22-22] Dir', True),
        ('Metal/Dir', False),
        ('Metal/[2222] Dir', False),
        ('Metal/[2222-22] Dir', False),
        ('Metal/[2222-22-22] ', False),
        ('Metal/[2222-22-22]', False),
    ])
    def test__check(self, file_name: str, is_valid: bool):
        sut = BadDirNameChecker('/mnt/music', self.filesystem)
        sut.check()

        issues = [x for x in sut.issues()]
        if is_valid:
            self.assertNotIn(file_name, issues)
        else:
            self.assertIn(file_name, issues)
