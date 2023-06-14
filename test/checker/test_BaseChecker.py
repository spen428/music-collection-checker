from unittest import TestCase

from checker import BaseChecker


class TestBaseChecker(TestCase):
    def test__constructor_assigns_correct_default_values(self):
        name = "The name of the checker"
        work_dir = "twenty/six/characters/long"

        sut = BaseChecker(name, work_dir, [])

        self.assertEqual(sut.name, name)
        self.assertEqual(sut.work_dir, work_dir)
        self.assertEqual(sut.work_dir_len, 26)
        self.assertEqual(sut._issues, [])

    def test__constructor_removes_unnecessary_characters_from_work_dir(self):
        sut = BaseChecker('', '/tmp/', [])
        self.assertEqual(sut.work_dir, '/tmp')

        sut = BaseChecker('', 'home///', [])
        self.assertEqual(sut.work_dir, 'home')

        sut = BaseChecker('', './bin///', [])
        self.assertEqual(sut.work_dir, 'bin')

        sut = BaseChecker('', '.bin', [])
        self.assertEqual(sut.work_dir, '.bin')

        sut = BaseChecker('', '/usr//bin', [])
        self.assertEqual(sut.work_dir, '/usr/bin')

    def test__log_issue_removes_work_dir_prefix(self):
        sut = BaseChecker('', './this/should/be/removed', [])
        sut._log_issue('./this/should/be/removed/this_is/my.issue')
        self.assertEqual(next(sut.issues()), 'this_is/my.issue')

    def test__pre_post_check_hooks_run_in_order(self):
        stack = []
        sut = BaseChecker('', '', [])
        sut._pre_check = lambda *args: stack.append("pre_check")
        sut._check = lambda *args: stack.append("check")
        sut._post_check = lambda *args: stack.append("post_check")

        sut.check()

        self.assertEqual("pre_check", stack[0])
        self.assertEqual("post_check", stack[-1])
        self.assertEqual(["check"], list(set(stack[1:-1])))
