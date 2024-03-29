import os
from unittest import TestCase

from StringToFilesystem import string_to_filesystem


def deeply_sorted(nested_list):
    return [(a, sorted(b), sorted(c)) for a, b, c in sorted(nested_list)]


class StringToFileSystemTests(TestCase):
    expected = [
        ('res/os_walk_test', ['.config'], ['.emacs']),
        ('res/os_walk_test/.config', ['evolution'], []),
        ('res/os_walk_test/.config/evolution', ['calendar', 'mail', 'memos', 'sources'], ['cert_trees.ini']),
        ('res/os_walk_test/.config/evolution/calendar', [], ['state.ini']),
        ('res/os_walk_test/.config/evolution/mail', ['folders'], ['state.ini']),
        ('res/os_walk_test/.config/evolution/mail/folders', [], []),
        ('res/os_walk_test/.config/evolution/memos', ['views'], ['state.ini']),
        ('res/os_walk_test/.config/evolution/memos/views', [], []),
        ('res/os_walk_test/.config/evolution/sources', [], ['local.source']),
    ]

    def test_os_walk_returns_expected_structure(self):
        path = 'res/os_walk_test'
        actual = deeply_sorted(os.walk(path))
        self.assertEqual(self.expected, actual)

    def test_os_walk_with_extra_slashes_preserves_slashes(self):
        path = 'res/os_walk_test///.config/evolution/mail/folders///'
        actual = deeply_sorted(os.walk(path))
        self.assertEqual([(path, [], [])], actual)

    def test_string_to_filesystem(self):
        string = """
res/os_walk_test/.config/
res/os_walk_test/.config/evolution/
res/os_walk_test/.config/evolution/calendar/
res/os_walk_test/.config/evolution/calendar/state.ini
res/os_walk_test/.config/evolution/cert_trees.ini
res/os_walk_test/.config/evolution/memos/
res/os_walk_test/.config/evolution/memos/state.ini
res/os_walk_test/.config/evolution/memos/views/
res/os_walk_test/.config/evolution/sources/
res/os_walk_test/.config/evolution/sources/local.source
res/os_walk_test/.config/evolution/mail/
res/os_walk_test/.config/evolution/mail/state.ini
res/os_walk_test/.config/evolution/mail/folders/
res/os_walk_test/.emacs
"""
        self.assertEqual(self.expected, string_to_filesystem(string, 'res/os_walk_test'))

    def test_string_to_filesystem_omitting_intermediate_dirs(self):
        string = """
res/os_walk_test/.config/evolution/calendar/state.ini
res/os_walk_test/.config/evolution/cert_trees.ini
res/os_walk_test/.config/evolution/memos/state.ini
res/os_walk_test/.config/evolution/memos/views/
res/os_walk_test/.config/evolution/sources/local.source
res/os_walk_test/.config/evolution/mail/state.ini
res/os_walk_test/.config/evolution/mail/folders/
res/os_walk_test/.emacs
"""
        self.assertEqual(self.expected, string_to_filesystem(string, 'res/os_walk_test'))

    def test_string_to_filesystem_root_dir_equals_string(self):
        expected = [('/mnt/music', [], [])]
        self.assertEqual(expected, string_to_filesystem('/mnt/music/', '/mnt/music/'))

    def test_string_to_filesystem_single_empty_subdir(self):
        expected = [('/mnt/music', ['sub_dir'], []), ('/mnt/music/sub_dir', [], [])]
        self.assertEqual(expected, string_to_filesystem('/mnt/music/sub_dir/', '/mnt/music/'))
