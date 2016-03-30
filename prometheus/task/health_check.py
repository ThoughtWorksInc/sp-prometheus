# coding: utf8

import time

from requests import request


class HeathCheckFailed(Exception):
    pass


class Task:
    def __init__(self, env):
        self.env = env

    def run(self, url, method="GET", content_type="application/json", status_code=200, **kwargs):
        time.sleep(10)
        res = request(method, url, headers={"Content-Type": content_type})
        if not (res and res.status_code == status_code):
            raise HeathCheckFailed()
