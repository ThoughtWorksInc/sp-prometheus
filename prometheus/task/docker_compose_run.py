# coding: utf8
import os.path
from subprocess import call


class Task:
    def __init__(self, env):
        self.env = env

    def docker_compose_run(self, compose_file, **kwargs):
        yaml_file = os.path.join(self.env.prometheus_path, compose_file)
        print "start run docker-compose: " + yaml_file
        call(["docker-compose", "-f", yaml_file, "up"])
        print "collect docker-compose resource"
        call(["docker-compose", "-f", yaml_file, "up"])
        call(["docker-compose", "-f", yaml_file, "rm", "-f"])
