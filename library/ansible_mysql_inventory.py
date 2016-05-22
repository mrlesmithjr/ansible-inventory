#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Larry Smith Jr.
# http://everythingshouldbevirtual.com
# @mrlesmithjr
# mrlesmithjr@gmail.com

import datetime
import MySQLdb
import sys
try:
    import json
except ImportError:
    import simplejson as json

# Define Vars
db_host = 'localhost'
db_name = 'ansible_inventory'
db_pass = 'ansible'
db_query = 'SELECT HostName,AnsibleSSHHost,HostDistribution,HostDistributionRelease,HostDistributionVersion,GroupName FROM inventory'
#db_query = 'SELECT * FROM inventory'
db_table = 'inventory'
db_user = 'ansible'

# Setup Connection
con = MySQLdb.connect(db_host, db_user, db_pass, db_name);

cur = con.cursor()
cur.execute(db_query)

#rows = cur.fetchall()

#for row in rows:
#    print row

for HostName, AnsibleSSHHost, HostDistribution, HostDistributionRelease, HostDistributionVersion, GroupName in cur:
#    print("inventory_hostname: {}, ansible_ssh_host: {}, group_names: {}").format(HostName,AnsibleSSHHost,GroupName)
    print(json.dumps({'inventory_hostname': HostName, 'ansible_ssh_host': AnsibleSSHHost, 'ansible_distribution': HostDistribution, \
    'ansible_distribution_release': HostDistributionRelease, 'ansible_distribution_version': HostDistributionVersion, 'group_names': GroupName}, \
    sort_keys=True, indent=4))
cur.close()
con.close()
