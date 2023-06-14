from unittest import TestCase

from parameterized import parameterized

from checker import BadDirNameChecker


class TestBadDirNameChecker(TestCase):

    @parameterized.expand([
        ('[2222-22-22] Dir', True),
        ('Dir', False),
        ('[2222] Dir', False),
        ('[2222-22] Dir', False),
        ('[2222-22-22] ', False),
        ('[2222-22-22]', False),
    ])
    def test__check(self, file_name: str, is_valid: bool):
        sut = BadDirNameChecker('')
        sut.check()

        issues = [x for x in sut.issues()]
        if is_valid:
            self.assertNotIn(file_name, issues)
        else:
            self.assertIn(file_name, issues)
