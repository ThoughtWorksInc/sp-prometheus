# coding: utf8
import unittest
import imp

import sys

from prometheus.prometheus import UnknownTaskException, IllegalTaskModuleException, TaskRunner


class TestTaskRunner(unittest.TestCase):
    def test_unknown_task(self):
        with self.assertRaises(UnknownTaskException):
            runner = TaskRunner({})
            runner.run('unknown')

    def test_illegal_task_module(self):
        mod = imp.new_module('prometheus.task.illegal_task_module')
        sys.modules['prometheus.task.illegal_task_module'] = mod

        with self.assertRaises(IllegalTaskModuleException):
            runner = TaskRunner({})
            runner.run('illegal_task_module')

