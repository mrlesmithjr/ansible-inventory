#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Larry Smith Jr.
# http://everythingshouldbevirtual.com
# @mrlesmithjr
# mrlesmithjr@gmail.com

# Import modules
import argparse
import datetime
import MySQLdb
import sys
try:
    import json
except ImportError:
    import simplejson as json

# Define classes
class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

# Setup arguments
parser = argparse.ArgumentParser(description='Ansible Inventory...')
parser.add_argument('-F','--function', help='Function to Execute, [default: all], valid choices: [groups | hosts | all | queryhost]',default='all',required=False)
parser.add_argument('-H','--host', help='Database Host, [default: 127.0.0.1]',default='127.0.0.1',required=False)
parser.add_argument('-P','--password', help='Database Password',required=True)
parser.add_argument('-QH','--queryhost', help='Query Host, Define Host to Query',required=False)
parser.add_argument('-U','--user', help='Database User',required=True)
args = parser.parse_args()

# Define Vars
db_name = 'ansible_inventory'

# Defined functions
def all_groups():
    db_query = 'SELECT GroupName FROM inventory'
    con = MySQLdb.connect(args.host, args.user, args.password, db_name);
    cur = con.cursor()
    cur.execute(db_query)
    rows = cur.fetchall()
    for row in rows:
        print(json.dumps(row))
    cur.close()
    con.close()

def all_hosts():
    db_query = 'SELECT HostName FROM inventory'
    con = MySQLdb.connect(args.host, args.user, args.password, db_name);
    cur = con.cursor()
    cur.execute(db_query)
    rows = cur.fetchall()
    for row in rows:
        print(json.dumps(row))
    cur.close()
    con.close()

def all_inventory():
    db_query = 'SELECT HostName,AnsibleSSHHost,HostDistribution,HostDistributionRelease,HostDistributionVersion,GroupName FROM inventory'
    con = MySQLdb.connect(args.host, args.user, args.password, db_name);
    cur = con.cursor()
    cur.execute(db_query)
    rows = cur.fetchall()
    for row in rows:
        print(json.dumps(row))
    cur.close()
    con.close()

def query_host():
    db_query = ('SELECT HostName,AnsibleSSHHost,GroupName FROM inventory WHERE HostName="%s"' %(args.queryhost))
    con = MySQLdb.connect(args.host, args.user, args.password, db_name);
    cur = con.cursor()
    cur.execute(db_query)
    rows = cur.fetchall()
    for HostName, AnsibleSSHHost, GroupName in cur:
        print(json.dumps({'host': HostName, 'ansible_ssh_host': AnsibleSSHHost, 'groups': GroupName}))
    cur.close()
    con.close()

# Decide which function to execute
if args.function == "all":
    all_inventory()
elif args.function == "groups":
    all_groups()
elif args.function == "hosts":
    all_hosts()
elif args.function == "queryhost":
    query_host()
