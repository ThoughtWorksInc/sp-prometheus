# coding: utf8
import os
import argparse
import tarfile
from io import BytesIO

from docker import Client
from .config_handler import ConfigHandler

CONFIG_FILE_NAME = "config.yml"
DEFAULT_CONFIG_DIR_NAME = "prometheus_ci"

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
            self.workspace, prometheus_path if prometheus_path else DEFAULT_CONFIG_DIR_NAME
        )
        print "got prometheus path: " + self.prometheus_path

        config_file = os.path.join(self.prometheus_path, CONFIG_FILE_NAME)
        with open(config_file) as f:
            self.configuration = ConfigHandler(f.read())

    def _build_image(self, dockerfile, workspace, image_name):
        for response in self.cli.build(
            dockerfile=dockerfile,
            path=workspace,
            tag=image_name,
            rm=True,
            nocache=True,
            decode=True
        ):
            if response.has_key('error'):
                raise Exception("Error building docker image: {}".format(response['error']))
            # print response.encode("utf-8")

    def _push_to_registry(self, image_name):
        print self.cli.push(image_name, insecure_registry=True)

    def __get_image_name(self, image_suffix, tag):

        return self.docker_registry + "/projects/" + self.configuration.project_name + "/" + image_suffix + ":" + tag

    def docker_build_and_publish(self, dockerfile, image_name, registry, workspace= "", **kwargs):
        print "start build image"
        dockerfile = os.path.join(
            self.prometheus_path, dockerfile
        )
        full_image_name = registry + "/" + image_name
        self._build_image(
            dockerfile, os.path.join(self.workspace, workspace), full_image_name
        )
        self._push_to_registry(full_image_name)

    def docker_run(self, image, command, archive=None, commit=None, copy_out=None, **kwargs):
        print "start run container"
        container = self.cli.create_container(image=image, command=command)
        try:
            self.cli.start(container.get("Id"))
            for log in self.cli.logs(container.get("Id"), stream=True):
                print log.encode("utf-8")
            if copy_out:
                copy_from = copy_out["from"]
                print "copy out files from: " + copy_from
                strm, stat = self.cli.get_archive(container.get("Id"), copy_from)
                print stat
                copy_to = copy_out["to"]
                print "extract to: " + copy_to
                tar = tarfile.open(fileobj=BytesIO(strm.read()))
                tar.extractall(copy_to)
            if commit:
                print "commit container: " + self.__get_image_name(commit["image_suffix"])
                self.cli.commit(container.get("Id"), tag=self.__get_image_name(commit["image_suffix"]))
        except Exception as e:
            print "run container exception: ", e
        finally:
            self.cli.remove_container(container.get("Id"), force=True)

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
