# coding: utf8
import tarfile
from io import BytesIO


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
                copy_from = copy_out["from"]
                print "copy out files from: " + copy_from
                strm, stat = self.env.cli.get_archive(container.get("Id"), copy_from)
                print stat
                copy_to = copy_out["to"]
                print "extract to: " + copy_to
                tar = tarfile.open(fileobj=BytesIO(strm.read()))
                tar.extractall(copy_to)
        except Exception as e:
            print "run container exception: ", e
        finally:
            self.env.cli.remove_container(container.get("Id"), force=True)
