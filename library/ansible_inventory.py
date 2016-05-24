#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Larry Smith Jr.
# http://everythingshouldbevirtual.com
# @mrlesmithjr
# mrlesmithjr@gmail.com

from __future__ import print_function

# Import modules
import argparse
import json
import MySQLdb

# Setup arguments
parser = argparse.ArgumentParser(description='Ansible Inventory...')
parser.add_argument('--addhost', required=False, help='Add Hostname')
parser.add_argument('--function', default='all', required=False,
                    help='Function to Execute...\n'
                    'valid function choices are\n'
                    '[addhost | all | groups | hosts | querygroup | queryhost]')
parser.add_argument('--host', default='127.0.0.1', required=False,
                    help='Database Host, [default: 127.0.0.1]')
parser.add_argument('--password', required=True, help='Database Password')
parser.add_argument('--querygroup', required=False,
                    help='Query Group, Define Group to Query')
parser.add_argument('--queryhost', required=False,
                    help='Query Host, Define Host to Query')
parser.add_argument('--user', required=True, help='Database User')
args = parser.parse_args()

# Define Vars
db_name = 'ansible_inventory'

# Defined functions
def add_host():
    sql = "INSERT INTO Hosts(HostName) VALUES('%s')" %(args.addhost)
    con = MySQLdb.connect(args.host, args.user, args.password, db_name)
    cur = con.cursor()
    try:
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()
    except MySQLdb.IntegrityError as e:
        print("IntegrityError")
        print(e)

def all_groups():
    sql = "SELECT DISTINCT GroupName FROM Groups"
    con = MySQLdb.connect(args.host, args.user, args.password, db_name)
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
    sql = "SELECT DISTINCT HostName FROM Hosts"
    con = MySQLdb.connect(args.host, args.user, args.password, db_name)
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
    sql = """
        SELECT HostName,AnsibleSSHHost,HostDistribution,
        HostDistributionRelease,HostDistributionVersion,
        GroupName FROM inventory"""
    con = MySQLdb.connect(args.host, args.user, args.password, db_name)
    cur = con.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    results = []
    results.append('inventory')
    for HostName, AnsibleSSHHost, HostDistribution, HostDistributionRelease, \
        HostDistributionVersion, GroupName in rows: \
        results.append({'host': HostName, 'ansible_ssh_host': AnsibleSSHHost, \
        'ansible_distribution': HostDistribution, \
        'ansible_distribution_release': HostDistributionRelease, \
        'ansible_distribution_version': HostDistributionVersion, \
        'groups': GroupName})
    print(json.dumps(results, sort_keys=True))
    cur.close()
    con.close()

def query_group():
    sql = """SELECT HostName,AnsibleSSHHost FROM inventory WHERE
        GroupName='%s' ORDER BY HostName""" %(args.querygroup)
    con = MySQLdb.connect(args.host, args.user, args.password, db_name)
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
    sql = """SELECT HostName,AnsibleSSHHost,GroupName FROM inventory
        WHERE HostName='%s'""" %(args.queryhost)
    con = MySQLdb.connect(args.host, args.user, args.password, db_name)
    cur = con.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    results = []
    results.append('inventory')
    for HostName, AnsibleSSHHost, GroupName in rows:
        results.append({'host': HostName, 'ansible_ssh_host': AnsibleSSHHost,
                        'groups': GroupName})
    print(json.dumps(results, sort_keys=True))
    cur.close()
    con.close()

# Decide which function to execute
if args.function == "addhost":
    add_host()
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
