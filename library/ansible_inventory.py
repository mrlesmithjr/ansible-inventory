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
parser.add_argument('-F','--function', help='Function to Execute, [default: all], valid choices: [groups | hosts | all | querygroup | queryhost]',default='all',required=False)
parser.add_argument('-H','--host', help='Database Host, [default: 127.0.0.1]',default='127.0.0.1',required=False)
parser.add_argument('-P','--password', help='Database Password',required=True)
parser.add_argument('-QG','--querygroup', help='Query Group, Define Group to Query',required=False)
parser.add_argument('-QH','--queryhost', help='Query Host, Define Host to Query',required=False)
parser.add_argument('-U','--user', help='Database User',required=True)
args = parser.parse_args()

# Define Vars
db_name = 'ansible_inventory'

# Defined functions
def all_groups():
    sql = 'SELECT DISTINCT GroupName FROM inventory'
    con = MySQLdb.connect(args.host, args.user, args.password, db_name);
    cur = con.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    results = []
    results.append('inventory')
    results.append('groups')
    for row in rows:
        results.append(row)
    print(json.dumps(results))
    cur.close()
    con.close()

def all_hosts():
    sql = 'SELECT DISTINCT HostName FROM inventory'
    con = MySQLdb.connect(args.host, args.user, args.password, db_name);
    cur = con.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    results = []
    results.append('inventory')
    results.append('hosts')
    for row in rows:
        results.append(row)
    print(json.dumps(results))
    cur.close()
    con.close()

def all_inventory():
    sql = 'SELECT HostName,AnsibleSSHHost,HostDistribution,HostDistributionRelease,HostDistributionVersion,GroupName \
    FROM inventory'
    con = MySQLdb.connect(args.host, args.user, args.password, db_name);
    cur = con.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    results = []
    results.append('inventory')
    for HostName, AnsibleSSHHost, HostDistribution, HostDistributionRelease, HostDistributionVersion, GroupName in rows:
        results.append({'host': HostName, 'ansible_ssh_host': AnsibleSSHHost, 'ansible_distribution': HostDistribution, \
        'ansible_distribution_release': HostDistributionRelease, 'ansible_distribution_version': HostDistributionVersion, \
        'groups': GroupName})
    print(json.dumps(results, sort_keys=True))
    cur.close()
    con.close()

def query_group():
    sql = ('SELECT HostName,AnsibleSSHHost FROM inventory WHERE GroupName="%s" ORDER BY HostName' %(args.querygroup))
    con = MySQLdb.connect(args.host, args.user, args.password, db_name);
    cur = con.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    results = []
    results.append('inventory')
    for HostName, AnsibleSSHHost in rows:
        results.append({'host': HostName, 'ansible_ssh_host': AnsibleSSHHost})
    print(json.dumps(results))
    cur.close()
    con.close()

def query_host():
    sql = ('SELECT HostName,AnsibleSSHHost,GroupName FROM inventory WHERE HostName="%s"' %(args.queryhost))
    con = MySQLdb.connect(args.host, args.user, args.password, db_name);
    cur = con.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    results = []
    results.append('inventory')
    for HostName, AnsibleSSHHost, GroupName in rows:
        results.append({'host': HostName, 'ansible_ssh_host': AnsibleSSHHost, 'groups': GroupName})
    print(json.dumps(results))
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
elif args.function == "querygroup":
    query_group()
