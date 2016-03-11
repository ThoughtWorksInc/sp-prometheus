# coding: utf8
import os


class Task:
    def __init__(self, env):
        self.env = env

    def run(self, dockerfile, image_name, registry, workspace="", **kwargs):
        print "start build image"
        dockerfile = os.path.join(self.env.prometheus_path, dockerfile)

        full_image_name = registry + "/" + image_name

        self.__build_image(dockerfile, os.path.join(self.env.workspace, workspace), full_image_name)

        self.__push_to_registry(full_image_name)

    def __build_image(self, dockerfile, workspace, image_name):
        for response in self.env.cli.build(
                dockerfile=dockerfile,
                path=workspace,
                tag=image_name,
                rm=True,
                nocache=True,
                decode=True
        ):
            if response.has_key('error'):
                raise Exception("Error building docker image: {}".format(response['error']))
                # print response.encode("utf-

    def __push_to_registry(self, image_name, insecure_registry=True):
        log = self.env.cli.push(image_name, insecure_registry=insecure_registry)
        print log
