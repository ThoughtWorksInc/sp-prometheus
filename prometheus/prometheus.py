# coding: utf8
import os
import argparse

from docker import Client


class Prometheus:
    def __init__(
        self,
        configuration_path=None,
        docker_host=None
    ):
        docker_host = docker_host or os.environ.get("DOCKER_HOST")
        print "got docker host: " + docker_host
        self.cli = Client(base_url=docker_host)
        print "got docker registry: " + os.environ.get("DOCKER_REGISTRY", "")
        self.docker_registry = os.environ.get("DOCKER_REGISTRY", "")
        print "got workspace: " + os.environ.get("WORKSPACE", "")
        self.workspace = os.environ.get("WORKSPACE", "")
        if configuration_path is None:
            configuration_path = os.path.join(self.workspace, "prometheus_ci")
        self.try_load_configuration(configuration_path)

    def try_load_configuration(self, configuration_path):
        try:
            config_file = os.path.join(configuration_path, "config")
            with open(config_file) as f:
                [setattr(
                    self, row.split("=", 1)[0], row.split("=", 1)[-1]
                ) for row in f.readlines()]
        except:
            pass

    def build_image(self, dockerfile_path, workbase_path, image_name):
        for log in self.cli.build(
            path=workbase_path,
            dockerfile=dockerfile_path,
            tag=image_name
        ):
            print log

    def push_to_registry(self, image_name):
        for log in self.cli.push(image_name):
            print log

    def __get_image_name(self, dockerfile_path, tag="latest"):
        return self.docker_registry + "/" + dockerfile_path.split(".")[-1] + ":" + tag

    def prepare_build_image(self, base, **kwargs):
        dockerfile = os.path.join(
            self.workspace, "prometheus_ci",
            "build_stage", "prepare_build_env",
            "Dockerfile.support_env"
        )
        image_name = self.__get_image_name(dockerfile)
        self.build_image(
            dockerfile, os.path.join(self.workspace, base), image_name
        )
        self.push_to_registry(image_name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("step")
    parser.add_argument("workspace")
    parser.add_argument("-path", help="special the prometheus config path")
    parser.add_argument("--base", help="workbase path", default="")
    parser.add_argument("--tag", help="tag")
    prometheus = Prometheus()
    try:
        result = parser.parse_args()
        if result.path:
            prometheus = Prometheus(result.path)
        else:
            prometheus = Prometheus()
        if hasattr(prometheus, result.step):
            getattr(prometheus, result.step)(tag=result.tag, base=result.base)
        else:
            print "unknown step" + result.step
    except Exception as e:
        print e
        exit(1)
