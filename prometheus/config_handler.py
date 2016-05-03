# coding: utf8

import re

import yaml


class NoSuchTaskException(Exception):
    def __init__(self, name):
        self.name = name


class NoHandlerException(Exception):
    def __init__(self, task):
        self.task = task


class ConfigHandler:
    TEMPLATE = re.compile(r"{{( )*(?P<key>\w+)( )*}}")
    def __init__(self, configuration, environments):
        if environments:
            configuration = self.inflate_environments(configuration, environments)

        self.configuration = yaml.load(configuration)
        for key, value in self.configuration.items():
            setattr(self, key, value)

    def inflate_environments(self, configuration, environments):
        mapping = yaml.load(environments)

        def inflate(matchobj):
            value = mapping.get(matchobj.group("key"))
            assert value, "miss environment: " + matchobj.group()
            return value

        return self.TEMPLATE.sub(inflate, configuration)

    def get_task(self, name):
        task = self.tasks.get(name)
        if task is None:
            raise NoSuchTaskException(name)
        runner = task.get("runner")
        if runner is None:
            raise NoHandlerException(name)
        return runner, task
