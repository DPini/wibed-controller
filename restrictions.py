from flask import session, redirect, url_for, abort,flash
import logging

def admin_required():
	if 'user' not in session:
		flash("Not logged in")
		return redirect(url_for('login'))
	if session['user'] != "admin":
		abort(401)

def user_required():
	if 'user' not in session:
		flash("Not logged in")
		return redirect(url_for('login'))
