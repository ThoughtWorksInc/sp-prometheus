# coding: utf8

import os
from subprocess import call, PIPE, Popen

from .base import export_file


class Task:
    def __init__(self, env):
        self.env = env

    def run(self, compose_file, copy_out=None, **kwargs):
        yaml_file = os.path.join(self.env.prometheus_path, compose_file)
        print "start run docker-compose: " + yaml_file
        os.environ["DOCKER_HOST"] = self.env.docker_host
        out, err = Popen(["docker-compose", "-f", yaml_file, "up", "--abort-on-container-exit"]).communicate()
        if err:
            raise RuntimeError()
        if copy_out:
            export_file(self.env.cli, copy_out["container_name"], copy_out["from"], copy_out["to"])
        print "collect docker-compose resource"
        out, err = Popen(
            ["docker-compose", "-f", yaml_file, "rm", "-f"],
            stdout=PIPE, stdin=PIPE, stderr=PIPE
        ).communicate()
        del os.environ["DOCKER_HOST"]
        print out
        # if err:
        #     print "error: " + err
        #     raise RuntimeError(err)
