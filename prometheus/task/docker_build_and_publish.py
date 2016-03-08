# coding: utf8
import os

import prometheus.docker.utils as utils


class Task:
    def __init__(self, env):
        self.env = env

    def run(self, dockerfile, image_name, registry, workspace="", **kwargs):
        print "start build image"
        dockerfile = os.path.join(self.env.prometheus_path, dockerfile)

        full_image_name = registry + "/" + image_name

        utils.build_image(self.env.cli, dockerfile, os.path.join(self.env.workspace, workspace), full_image_name)

        utils.push_to_registry(self.env.cli, full_image_name)
