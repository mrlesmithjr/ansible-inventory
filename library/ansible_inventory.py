#!/usr/bin/env python
"""ansible_inventory.py: Query/Manage Ansible Facts

   This script will query or manage Ansible Facts into a useable inventory"""

# Import modules
import argparse
import json
import MySQLdb

__author__ = "Larry Smith Jr."
__email___ = "mrlesmithjr@gmail.com"
__maintainer__ = "Larry Smith Jr."
__status__ = "Development"
# http://everythingshouldbevirtual.com
# @mrlesmithjr

class AnsibleMySQL(object):
    """ Setup Main execution """

    def __init__(self):

        self.read_cli_args()

        if self.args.all:
            self.all_inventory()
        elif self.args.allgroups:
            self.all_groups()
        elif self.args.allhosts:
            self.all_hosts()
        elif self.args.querygroup:
            self.query_group()
        elif self.args.queryhost:
            self.query_host()
        else:
            self.all_inventory()

        self.con = MySQLdb.connect(self.args.host, self.args.user,
                                   self.args.password, self.args.db)
        self.cur = self.con.cursor()
        self.cur.execute(self.sql)
        self.rows = self.cur.fetchall()
        self.cur.close()
        self.con.close()
        self.process_results()

    def all_groups(self):
        """Query all groups

        This will query all groups in the inventory and return the results.

        Ex.
        ansible_inventory.py --user ansible --password --ansible --allgroups
        """

        self.sql = "SELECT DISTINCT GroupName FROM Groups"

    def all_hosts(self):

        """Query all hosts

        This will query all hosts in the inventory and return the results.

        Ex.
        ansible_inventory.py --user ansible --password ansible --allhosts
        """

        self.sql = "SELECT DISTINCT HostName FROM Hosts"

    def all_inventory(self):

        """Query all hosts/groups

        This will query all hosts/groups in the inventory and return the results.
        This is also the default when executed as below...
        ansible_inventory.py --user ansible --password ansible

        Ex.
        ansible_inventory.py --user ansible --password ansible
          or
         ansible_inventory.py --user ansible --password ansible --all
        """

        self.sql = """
            SELECT HostName,AnsibleSSHHost,HostDistribution,
            HostDistributionRelease,HostDistributionVersion,
            GroupName FROM inventory"""

    def process_results(self):

        """ Process and display results of the query"""

        self.results = []
        for self.row in self.rows:
            self.results.append(self.row)
        print json.dumps(self.results, sort_keys=True)

    def query_group(self):

        """Query a specific group

        This will query a specific group and return the results.

        Ex.
        ansible_inventory.py --user ansible --password ansible
            --querygroup test-nodes

        Keyword arguments:
        args.querygroup -- actual group to query
        """

        self.sql = """
            SELECT HostName,AnsibleSSHHost FROM inventory WHERE
            GroupName='%s' ORDER BY HostName""" %(self.args.querygroup)

    def query_host(self):

        """Query a specific host

        This will query a specific group and return the results.

        Ex.
        ansible_inventory.py --user ansible --password ansible --queryhost node0

        Keyword arguments:
        args.queryhost -- actual host to query
        """

        self.sql = """
            SELECT HostName,AnsibleSSHHost,GroupName FROM inventory
            WHERE HostName='%s'""" %(self.args.queryhost)

    def read_cli_args(self):
        """ Setup and Read Command Line Arguments to Pass"""

        parser = argparse.ArgumentParser(description='Ansible Inventory...')
        parser.add_argument('--all', help='Display all inventory items',
                            action='store_true')
        parser.add_argument('--allgroups', help='Display all groups',
                            action='store_true')
        parser.add_argument('--allhosts', help='Display all hosts',
                            action='store_true')
        parser.add_argument('--db', default='ansible_inventory',
                            help='Database Name')
        parser.add_argument('--host', default='127.0.0.1',
                            help='Database Host, [default: 127.0.0.1]')
        parser.add_argument('--password', required=True,
                            help='Database Password')
        parser.add_argument('--querygroup',
                            help='Query Group, Define Group to Query')
        parser.add_argument('--queryhost',
                            help='Query Host, Define Host to Query')
        parser.add_argument('--user', required=True, help='Database User')
        self.args = parser.parse_args()

AnsibleMySQL()
