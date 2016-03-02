# coding: utf8
import os
import unittest

from prometheus.config_handler import ConfigHandler


class TestConfigHandler(unittest.TestCase):
    def test_load_config_based(self):
        configuration = '''
        tasks:
            release:
                handler: build_image
                image_suffix: release
                docker_file: ./dockerfile
                workspace: .
        '''
        configHandler = ConfigHandler(configuration)
        self.assertTrue(configHandler.configuration is not None)

    def test_success_get_task_release(self):
        configuration = '''
        tasks:
            release:
                handler: build_image
                image_suffix: release
                docker_file: ./dockerfile
                workspace: .
        '''
        configHandler = ConfigHandler(configuration)
        handler, params = configHandler.get_task("release")

        self.assertEquals(handler, "build_image")
        self.assertTrue("image_suffix" in params)