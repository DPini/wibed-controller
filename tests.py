# this tests require Flask-Testing to be installed

import unittest
import json
from flask.ext.testing import TestCase
from flask import jsonify

from server import create_app
from database import db

from models.node import Node
from models.experiment import Experiment
from models.command import Command
from models.execution import Execution
from models.firmware import Firmware

INIT, IDLE, PREPARING, READY, RUNNING, UPGRADING, ERROR = 0, 1, 2, 3, 4, 5, 6

class WibedTest(TestCase):

    def create_app(self):
        return create_app("settings.TestingConfig")

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
#        db.drop_app()

class ApiTest(WibedTest):

    def post_node(self, node_id="anode", status=INIT):
        response = self.client.post(
            "/api/wibednode/"+ node_id,
            data=json.dumps(dict(model="mymodel", version="1.0", status=status)))
        return response

    def test_node_creation(self):
        node_id = "mynode"
        response = self.post_node(node_id)
        node = Node.query.get(node_id)
        self.assert200(response)
        self.assertEquals(response.json, {})
        assert node in db.session

    def test_node_update(self):
        node_id = "mynode"
        response = self.post_node(node_id)
        node = Node.query.get(node_id)
        self.assertEquals(node.status, Node.Status.INIT)
        response = self.post_node(node_id, IDLE)
        node = Node.query.get(node_id)
        self.assertEquals(node.status, Node.Status.IDLE)
        

if __name__ == '__main__':
    unittest.main()
