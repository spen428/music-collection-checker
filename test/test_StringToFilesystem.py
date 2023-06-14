import os
from unittest import TestCase

from StringToFilesystem import string_to_walk_list


def deeply_sorted(nested_list):
    return [(a, sorted(b), sorted(c)) for a, b, c in sorted(nested_list)]


class Test(TestCase):
    expected = [
        ('.config', ['evolution'], []),
        ('.config/evolution', ['calendar', 'mail', 'memos', 'sources'], ['cert_trees.ini']),
        ('.config/evolution/calendar', [], ['state.ini']),
        ('.config/evolution/mail', ['folders'], ['state.ini']),
        ('.config/evolution/mail/folders', [], []),
        ('.config/evolution/memos', ['views'], ['state.ini']),
        ('.config/evolution/memos/views', [], []),
        ('.config/evolution/sources', [], ['local.source']),
    ]

    def test_os_walk_returns_expected_structure(self):
        actual = deeply_sorted(os.walk('.config'))
        self.assertEqual(self.expected, actual)

    def test_string_to_walk_list(self):
        string = """.config/
.config/evolution/
.config/evolution/calendar/
.config/evolution/calendar/state.ini
.config/evolution/cert_trees.ini
.config/evolution/memos/
.config/evolution/memos/state.ini
.config/evolution/memos/views/
.config/evolution/sources/
.config/evolution/sources/local.source
.config/evolution/mail/
.config/evolution/mail/state.ini
.config/evolution/mail/folders/
"""
        self.assertEqual(self.expected, string_to_walk_list(string))
