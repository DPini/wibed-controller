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
    maxDiff = None
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

    def create_experiment(self, name="anexperiment", nodes=[], overlay=""):
        if not nodes:
            nodes = [self.create_node()]
        experiment = Experiment(
            name=name,
            overlay=overlay,
            nodes=nodes
            )
        db.session.add(experiment)
        db.session.commit()
        return experiment

    def create_command(self, command_line="echo OK", experimentId=None, nodes=[]):
        if not experimentId:
            experiment = self.create_experiment(nodes=nodes)
            experimentId = experiment.id
        command = Command(command_line, experimentId)
        db.session.add(command)
        db.session.commit()
        return command

    def fake_exec(self, commandId, node=None, exitCode=0, stdout="OK", stderr=""):
        if not node:
            node = Node.query.one()
        execution = Execution(commandId, node.id, 0, stdout, stderr)
        db.session.add(execution)
        db.session.commit()

class NodeApiTest(WibedTest):

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

class CommandApiTest(WibedTest):

    def test_command_output(self):
        command = self.create_command()
        self.fake_exec(command.id)
        with self.app.test_client() as c:
            response = c.get("/api/commandOutput/" + str(command.id))
            self.assertEquals(response.json,
                {"commandId": 1,
                 "command": "echo OK",
                 "executions":
                     [{"node": 'anode',
                      "result":
                          {"exitCode": 0,
                           "stdout": 'OK',
                           "stderr": ''
                          }
                      }]
                })

class ExperimentApiTest(WibedTest):

    def test_experiment_info(self):
        node = self.create_node()
        experiment = self.create_experiment(nodes=[node])
        command = self.create_command(experimentId=experiment.id)
        with self.app.test_client() as c:
            response = c.get("/api/experimentInfo/" + str(experiment.id))
            self.assertEquals(response.json,
                              { str(experiment.id): {'nodes':[node.id],
                                                 'commands': [command.id]}})
    def test_experiment_output(self):
        node = self.create_node()
        experiment = self.create_experiment(nodes=[node])
        command = self.create_command(experimentId=experiment.id)
        self.fake_exec(command.id)
        with self.app.test_client() as c:
            response = c.get("/api/experimentOutput/" + str(experiment.id))
            self.assertEquals(response.json,
                {"experimentId": experiment.id,
                 "experiment": experiment.name,
                 "commands": [{
                    "commandId": 1,
                     "command": "echo OK",
                     "executions":
                         [{"node": 'anode',
                          "result":
                              {"exitCode": 0,
                               "stdout": 'OK',
                               "stderr": ''
                              }
                          }]
                 }]
                })

class NodeModelTest(WibedTest):

    def test_node_reachable(self):
        node_id = "mynode"
        response = self.post_node(node_id)
        node = Node.query.get(node_id)
        self.assertEquals(node.reachable, True)
        response = self.post_node(node_id, IDLE)
        sleep(1) # the REACHABLE_WINDOW is set to 1 in TestingConfig
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
            experiment = self.create_experiment("myexperiment", [node])
            db.session.add(experiment)
            db.session.commit()
            response = c.get("/experiment/show/1")
            assert "secs. ago" in response.data


if __name__ == '__main__':
    unittest.main()
