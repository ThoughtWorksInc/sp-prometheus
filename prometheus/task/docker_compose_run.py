# coding: utf8
import os.path
from subprocess import call, PIPE, Popen


class Task:
    def __init__(self, env):
        self.env = env

    def run(self, compose_file, **kwargs):
        yaml_file = os.path.join(self.env.prometheus_path, compose_file)
        print "start run docker-compose: " + yaml_file
        out, err = Popen(["docker-compose", "-f", yaml_file, "up", "--abort-on-container-exit"]).communicate()
        if err:
            raise RuntimeError()
        print "collect docker-compose resource"
        out, err = Popen(
            ["DOCKER_HOST="+self.env.docker_host, "docker-compose", "-f", yaml_file, "rm", "-f"],
            stdout=PIPE, stdin=PIPE, stderr=PIPE
        ).communicate()
        print out
        # if err:
        #     print "error: " + err
        #     raise RuntimeError(err)
