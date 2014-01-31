from flask import session
from models.node import Node
import logging


def get_nodes(custom_filter):
	if custom_filter:
		if session['user'] != "admin":
			nodes = eval("Node.query.filter("+custom_filter+", Node.show == True)")
			return nodes 
		else:
			nodes = eval("Node.query.filter("+custom_filter+")")
			return nodes
	else :
		if session['user'] != "admin":
			return Node.query.filter(Node.show == True)
		else:
			return Node.query.all()

		
