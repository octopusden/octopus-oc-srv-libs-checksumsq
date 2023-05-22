import unittest
from ..checksums_interface import ChecksumsQueueClient
from oc_cdt_queue2.test.synchron.mocks.queue_loopback import LoopbackConnection
from argparse import ArgumentParser


class TestClient(ChecksumsQueueClient):
    def _basic_publish(self, body, content_type, headers, content_encoding):
        self.myroutingkey += [ self.routing_key ]


class ChecksumsQueueClientTest(unittest.TestCase):

    def test_double_queue(self):
        client = TestClient()
        client._Connection = LoopbackConnection

        parser = client.basic_args(ArgumentParser('test'))

        args = parser.parse_args('--amqp-url amqp://127.0.0.1/ --declare yes --queue my --queue-cnt my1'.split(' '))

        client.setup_from_args(args)
        client.connect()
        client.myroutingkey = []

        client.register_file('somewhere','OTHER',3)

        self.assertEqual(len(client.myroutingkey), 2)
        self.assertEqual(client.myroutingkey[0], 'my')
        self.assertEqual(client.myroutingkey[1], 'my1')


