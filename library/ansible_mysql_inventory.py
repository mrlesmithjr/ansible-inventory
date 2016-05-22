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

# Setup arguments
parser = argparse.ArgumentParser(description='Ansible Inventory...')
parser.add_argument('-H','--host', help='Database Host',required=True)
parser.add_argument('-U','--user', help='Database User',required=True)
parser.add_argument('-P','--password', help='Database Password',required=True)
args = parser.parse_args()

# Define Vars
db_name = 'ansible_inventory'
db_query = 'SELECT HostName,AnsibleSSHHost,HostDistribution,HostDistributionRelease,HostDistributionVersion,GroupName FROM inventory'
db_table = 'inventory'

# Setup Connection
con = MySQLdb.connect(args.host, args.user, args.password, db_name);

cur = con.cursor()
cur.execute(db_query)

#rows = cur.fetchall()

#for row in rows:
#    print row

for HostName, AnsibleSSHHost, HostDistribution, HostDistributionRelease, HostDistributionVersion, GroupName in cur:
#    print("inventory_hostname: {}, ansible_ssh_host: {}, group_names: {}").format(HostName,AnsibleSSHHost,GroupName)
    print(json.dumps({'inventory_hostname': HostName, 'ansible_ssh_host': AnsibleSSHHost, 'ansible_distribution': HostDistribution, \
    'ansible_distribution_release': HostDistributionRelease, 'ansible_distribution_version': HostDistributionVersion, 'group_names': GroupName}))
cur.close()
con.close()
