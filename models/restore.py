""" Resetting process """

from enum import Enum

from database import db, DatabaseEnum
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from models.node import Node
import logging

class Restore(db.Model):
	"""
	Represents the resetting process of a node intiated
	by another node.
	"""

	__table_args__ = {'sqlite_autoincrement': True}

	Status = Enum("Status", {"IDLE":0, "SENDRESTORE":1, "RESTORING":2})

        #	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        # If dest_id only is the primary (still have ids but dest_id is 
        # unique) then nodes can have only one reset
        # Alternatively nodes could have dest_id and source_id as primary
        # keys or both unique where nodes can have one reset per GW but
        # this is complicated to handle
	dest_id = db.Column(db.String(64), db.ForeignKey('node.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
        source_id = db.Column(db.String(64), db.ForeignKey('node.id', onupdate="CASCADE", ondelete="CASCADE"))
	status = db.Column(DatabaseEnum(Status, *[e.name for e in Status]))
	reset = db.Column(db.Boolean) 
	

	source = db.relationship("Node", foreign_keys=source_id, backref=db.backref("source_restore"))
	dest = db.relationship("Node", foreign_keys=dest_id, backref=db.backref("dest_restore"))	


	def __init__(self, dest, reset=False):
		if dest.reachable:
			raise Exception("Node is online, no reason for restore")
		self.dest_id = dest.id
		self.source_id = self.findNodeGwId(dest)
		self.reset = True if reset else False
		self.status = Restore.Status.IDLE

	def __repr__ (self):
		return "<Restore process of node %s by node %s, Status: %s >" % (self.dest_id, self.source_id, self.status)

	def start(self):
		if self.status != Restore.Status.IDLE:
			raise Exception("Restore cannot be initiated with status: %s" % self.status)
		self.status = Restore.Status.SENDRESTORE
		logging.debug("RESTORE: IDLE -> SENDRESTORE")

	def toRestore(self):
		if self.status != Restore.Status.SENDRESTORE:
			raise Exception("Restore cannot proceed if message was not sent to GW (status %s)" % self.status)
		self.status = Restore.Status.RESTORING
		logging.debug("RESTORE: SENDRESTORE -> RESTORING")

	def findNodeGwId (self,node):
		try:
			gw = Node.query.filter(Node.gateway == True).\
					filter(Node.address == node.gwaddress).one()
		except (MultipleResultsFound, NoResultFound), e:
			raise Exception("Error finding responsible GW: " % e)
		return gw.id
		
