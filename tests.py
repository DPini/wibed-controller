# this tests require Flask-Testing to be installed

import unittest
import json
from time import sleep
from datetime import datetime
from flask.ext.testing import TestCase

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

    def post_node(self, node_id="anode", status=INIT):
        response = self.client.post(
            "/api/wibednode/"+ node_id,
            data=json.dumps(dict(model="mymodel",
                                 version="1.0", status=status)))
        return response

    def create_node(self, node_id="anode"):
        node = Node(id=node_id)
        node.lastContact = datetime.now()
        node.status = Node.Status.IDLE
        db.session.add(node)
        db.session.commit()
        return node

class ApiTest(WibedTest):

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

class NodeModelTest(WibedTest):

    def test_node_reachable(self):
        node_id = "mynode"
        response = self.post_node(node_id)
        node = Node.query.get(node_id)
        self.assertEquals(node.reachable, True)
        response = self.post_node(node_id, IDLE)
        sleep(1) # the REACHABLE_WINDOW equals 1 in TestingConfig
        self.assertEquals(node.reachable, False)

class NodeListViewTest(WibedTest):

    def test_node_list(self):
        with self.app.test_client() as c:
            self.create_node()
            response = c.get("/node/list")
            assert "secs. ago" in response.data

class NodeShowViewTest(WibedTest):

    def test_node_show(self):
        with self.app.test_client() as c:
            self.create_node()
            response = c.get("/node/show/anode")
            assert "secs. ago" in response.data

class ExperimentShowViewTest(WibedTest):

    def test_experiment_show(self):
        with self.app.test_client() as c:
            node = self.create_node()
            experiment = Experiment(
                name="myexperiment",
                overlay="",
                nodes=[node]
                )
            db.session.add(experiment)
            db.session.commit()
            response = c.get("/experiment/show/1")
            assert "secs. ago" in response.data


if __name__ == '__main__':
    unittest.main()
