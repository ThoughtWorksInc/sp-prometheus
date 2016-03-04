# coding: utf8
import os
import argparse

from docker import Client

from .config_handler import ConfigHandler


class UnknownHandlerException(Exception):
    def __init__(self, name):
        self.name = name


class Prometheus:
    def __init__(
        self,
        prometheus_path=None,
        docker_host=None,
    ):
        docker_host = docker_host or os.environ.get("DOCKER_HOST")
        print "got docker host: " + docker_host
        self.cli = Client(base_url=docker_host)
        print "got docker registry: " + os.environ.get("DOCKER_REGISTRY", "")
        self.docker_registry = os.environ.get("DOCKER_REGISTRY", "")
        print "got workspace: " + os.environ.get("WORKSPACE", "")
        self.workspace = os.environ.get("WORKSPACE", "")
        self.prometheus_path = os.path.join(
            self.workspace, prometheus_path if prometheus_path else "prometheus_ci"
        )
        print "got prometheus path: " + self.prometheus_path

        config_file = os.path.join(self.prometheus_path, "config.yml")
        with open(config_file) as f:
            self.configuration = ConfigHandler(f.read())

    def _build_image(self, dockerfile, workspace, image_name):
        for log in self.cli.build(
            dockerfile=dockerfile,
            path=workspace,
            tag=image_name
        ):
            print log

    def _push_to_registry(self, image_name):
        print self.cli.push(image_name)

    def __get_image_name(self, image_suffix, tag):
        return self.docker_registry + "/projects/" + self.configuration.project_name + "/" + image_suffix + ":" + tag

    def build_image(self, dockerfile, image_suffix, workspace= "", tag="latest", **kwargs):
        dockerfile = os.path.join(
            self.prometheus_path, dockerfile
        )
        image_name = self.__get_image_name(image_suffix, tag)
        self._build_image(
            dockerfile, os.path.join(self.workspace, workspace), image_name
        )
        self._push_to_registry(image_name)

    def run_container(self, image, command, **kwargs):
        container = self.create_container(image=image, command=command)

    def run(self, task):
        task_runner, params = self.configuration.get_task(task)
        if not hasattr(self, task_runner):
            raise UnknownHandlerException(task_runner)

        getattr(self, task_runner)(**params)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("task")
    parser.add_argument("--path", help="special the prometheus config path")
    result = parser.parse_args()

    prometheus = Prometheus(result.path)
    prometheus.run(result.task)
