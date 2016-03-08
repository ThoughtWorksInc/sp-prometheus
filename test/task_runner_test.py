# coding: utf8
import unittest
import imp

import sys

from prometheus.config_handler import ConfigHandler
from prometheus.prometheus import UnknownTaskException, IllegalTaskModuleException, TaskRunner, TaskEnv


class TestTaskRunner(unittest.TestCase):
    def gen_test_env(self, config):
        configHandler = ConfigHandler(config)
        return TaskEnv(
            cli=None,
            prometheus_path='',
            workspace='',
            docker_registry='',
            docker_host='',
            configuration=configHandler
        )

    def test_unknown_task(self):
        env = self.gen_test_env('''
        tasks:
            test:
                runner: unknown
                dockerfile: dockerfile
                image_name: image_name
                registry: registry
        ''')

        with self.assertRaises(UnknownTaskException):
            runner = TaskRunner(env)
            runner.run('test')

    def test_illegal_task_module(self):
        mod = imp.new_module('prometheus.task.illegal_task_module')
        sys.modules['prometheus.task.illegal_task_module'] = mod

        env = self.gen_test_env('''
        tasks:
            test:
                runner: illegal_task_module
                dockerfile: dockerfile
                image_name: image_name
                registry: registry
        ''')

        with self.assertRaises(IllegalTaskModuleException):
            runner = TaskRunner(env)
            runner.run('test')

    def test_normal_task(self):
        env = self.gen_test_env('''
        tasks:
            test:
                runner: normal_task
                dockerfile: dockerfile
                image_name: image_name
                registry: registry
        ''')
        mod = imp.new_module('prometheus.task.normal_task')
        mod_code = '''
class Task:
    def __init__(self, env):
        pass

    def run(self, **kwargs):
        pass

        '''

        exec mod_code in mod.__dict__
        sys.modules['prometheus.task.normal_task'] = mod

        runner = TaskRunner(env)
        runner.run('test')
