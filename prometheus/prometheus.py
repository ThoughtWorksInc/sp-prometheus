# coding: utf8
import argparse
import os

from docker import Client
from .config_handler import ConfigHandler

CONFIG_FILE_NAME = "config.yml"
DEFAULT_CONFIG_DIR_NAME = "prometheus_ci"


class UnknownTaskException(Exception):
    def __init__(self, name):
        self.name = name


class IllegalTaskModuleException(Exception):
    def __init__(self, name):
        self.name = name


class TaskEnv:
    def __init__(self, cli, prometheus_path, workspace, docker_registry, docker_host, configuration):
        self.cli = cli
        self.prometheus_path = prometheus_path
        self.workspace = workspace
        self.docker_registry = docker_registry
        self.docker_host = docker_host
        self.configuration = configuration


class TaskRunner:
    def __init__(self, env):
        self.env = env

    def run(self, task_name):
        task_runner, task_config = self.env.configuration.get_task(task_name)

        try:
            mod = __import__('prometheus.task.' + task_runner)
            cls = getattr(mod, 'Task')
            task = cls(self.env)
            return getattr(task, 'run')(**task_config)
        except ImportError:
            raise UnknownTaskException(task_runner)
        except AttributeError:
            raise IllegalTaskModuleException(
                'Module does not contain Task class: ' + 'prometheus.task.' + task_runner + '_runner')


def init_env(prometheus_path=None,
             docker_host=None):
    docker_host = docker_host or os.environ.get("DOCKER_HOST")

    cli = Client(base_url=docker_host)

    docker_registry = os.environ.get("DOCKER_REGISTRY", "")

    workspace = os.environ.get("WORKSPACE", "")
    prometheus_path = os.path.join(
        workspace, prometheus_path if prometheus_path else DEFAULT_CONFIG_DIR_NAME
    )

    config_file = os.path.join(prometheus_path, CONFIG_FILE_NAME)
    with open(config_file) as f:
        configuration = ConfigHandler(f.read())

    return TaskEnv(
        cli=cli,
        prometheus_path=prometheus_path,
        workspace=workspace,
        docker_registry=docker_registry,
        docker_host=docker_host,
        configuration=configuration
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("task")
    parser.add_argument("--path", help="special the prometheus config path")
    result = parser.parse_args()

    env = init_env(result.path)
    print 'Script environment initialized: ' + str(env.__dict__)

    runner = TaskRunner(env)
    runner.run(result.task)
