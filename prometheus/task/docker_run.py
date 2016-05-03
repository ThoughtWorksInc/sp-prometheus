# coding: utf8

from .base import export_file


class Task:
    def __init__(self, env):
        self.env = env

    def run(self, image, command, copy_out=None, **kwargs):
        print "start run container"
        container = self.env.cli.create_container(image=image, command=command)
        try:
            self.env.cli.start(container.get("Id"))
            for log in self.env.cli.logs(container.get("Id"), stream=True):
                print log.encode("utf-8")
            if copy_out:
                export_file(self.env.cli, container.get("Id"), copy_out["from"], copy_out["to"])
        except Exception as e:
            print "run container exception: ", e
        finally:
            self.env.cli.remove_container(container.get("Id"), force=True)
