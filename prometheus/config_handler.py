# coding: utf8

import yaml


class NoSuchTaskException(Exception):
    def __init__(self, name):
        self.name = name


class NoHandlerException(Exception):
    def __init__(self, task):
        self.task = task


class ConfigHandler:
    def __init__(self, configuration):
        self.configuration = yaml.load(configuration)
        for key, value in self.configuration.items():
            setattr(self, key, value)

    def get_task(self, name):
        task = self.tasks.get(name)
        if task is None:
            raise NoSuchTaskException(name)
        runner = task.get("runner")
        if runner is None:
            raise NoHandlerException(name)
        return runner, task
