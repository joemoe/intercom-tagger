#!/usr/bin/env python3

import sys
import getopt
import os
import argparse
from intercom.client import Client
from intercom.errors import IntercomError
from crate import client

def parse_args():
    parser = argparse.ArgumentParser(description='''
    	This tool creates Intercom Tags and adds users to them based on a given list of
    	attributes.
    	When using this tool you need to make sure INTERCOM_ACCESS_TOKEN is set as 
    	system var containing the intercom access token.
    ''')
    parser.add_argument("-f", dest="filename", default=None,
    	help="The name of a file containing user_id token per line.")
    parser.add_argument("-q", dest="query", default=None, 
    	help="A query that selects one row containing an attribute value.")
    parser.add_argument("-a", dest="attribute", default="user_id",
    	help="The attribute the values match, defaults to \"user_id.\"")
    parser.add_argument("-t", dest="tag", default=None,
    	help="The tag the users should be mapped to. If the tag doesn't exist, it is created.")
    parser.add_argument("-c", dest="hosts", default=None,
    	help="A comma separated list of CrateDB hosts.")
    return parser.parse_args()

def main():
	file = None
	query = None
	hosts = None
	attribute = "user_id"
	tag_name = "test"

	users = []

	ns = parse_args()

	if ns.filename is not None:
		if os.path.exists(ns.filename):
			file = ns.filename
		else:
			print("File does not exist.")
	query = ns.query
	tag_name = ns.tag
	hosts = ns.hosts
	attribute = ns.attribute

	access_token = os.environ.get("INTERCOM_ACCESS_TOKEN")

	if access_token is None:
		print("Please make sure to set INTERCOM_ACCESS_TOKEN as a system var.")
		sys.exit(1)

	intercom = Client(personal_access_token=access_token)

	if file is not None:
		print("Checking users for file: " + file)
		for c in open(file):
			try:
				params = { attribute: c }
				intercom.users.find(**params)
				users.append({ attribute: c })
				print(c + " found and added")
			except IntercomError:
				print(c + " not found")


	if query is not None and hosts is not None:
		print("Checking users for query: " + query + "")
		connection = client.connect(hosts)
		cursor = connection.cursor()
		cursor.execute(query)

		print("> Fetching data from CrateDB")
		data = cursor.fetchall()
		print("> Checking existence of {} users".format(len(data)))
		for row in data:
			try:
				params = { attribute: row[0] }
				u = intercom.users.find(**params)
				users.append({ attribute: row[0]})
				print(row[0] + " found")
			except IntercomError:
				print(row[0] + " not found")


	if len(users):
		try:
			tag = intercom.tags.tag(name=tag_name, users=users)
			print("..........................................")
			print("Tag updated")
		except IntercomError:
			print("There was an error adding the users to the tag")
	else:
		print("..........................................")
		print("No user added")


if __name__ == "__main__":
	main()