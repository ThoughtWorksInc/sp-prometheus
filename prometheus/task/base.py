# coding: utf8

import tarfile
from io import BytesIO


def export_file(cli, container, copy_from, copy_to):
    print "copy out files from: " + copy_from
    strm, stat = cli.get_archive(container, copy_from)
    print stat
    print "extract to: " + copy_to
    tar = tarfile.open(fileobj=BytesIO(strm.read()))
    tar.extractall(copy_to)
