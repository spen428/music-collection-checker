from unittest import TestCase

from checker import BaseChecker


class TestBaseChecker(TestCase):
    def test__constructor_assigns_correct_default_values(self):
        name = "The name of the checker"
        work_dir = "twenty/six/characters/long"

        sut = BaseChecker(name, work_dir)

        assert sut.name == name
        assert sut.work_dir == work_dir
        assert sut.work_dir_len == 26
        assert sut._issues == []

    def test__constructor_removes_unnecessary_characters_from_work_dir(self):
        sut = BaseChecker('', '/tmp/')
        assert sut.work_dir == '/tmp'

        sut = BaseChecker('', 'home///')
        assert sut.work_dir == 'home'

        sut = BaseChecker('', './bin///')
        assert sut.work_dir == 'bin'

        sut = BaseChecker('', '.bin')
        assert sut.work_dir == '.bin'

        sut = BaseChecker('', '/usr//bin')
        assert sut.work_dir == '/usr/bin'

    def test__log_issue_removes_work_dir_prefix(self):
        sut = BaseChecker('', './this/should/be/removed')
        sut._log_issue('./this/should/be/removed/this_is/my.issue')
        assert next(sut.issues()) == 'this_is/my.issue'
