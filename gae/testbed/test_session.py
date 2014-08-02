import unittest

from google.appengine.ext import testbed as gae_testbed


class TestbedTestCase(unittest.TestCase):
    # whether to enable the datastore stub by default
    datastore = True
    # whether to enable the memcache stub by default
    memcache = True
    # whether to enable the tasks stub by default
    tasks = True

    def setUp(self):
        self.testbed = gae_testbed.Testbed()

        self.testbed.activate()
        self.addCleanup(self.testbed.deactivate)

        self.setUpServices(self.testbed)

    def setUpServices(self, testbed):
        if self.datastore:
            testbed.init_datastore_v3_stub()

        if self.memcache:
            testbed.init_memcache_stub()

        if self.tasks:
            testbed.init_taskqueue_stub()
