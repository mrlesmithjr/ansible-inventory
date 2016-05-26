#!/usr/bin/env python
"""
ansible_inventory.py: Query/Manage Ansible Facts

This script will query or manage Ansible Facts into a useable inventory
"""

# Import modules
import argparse
import datetime
import json
import MySQLdb

__author__ = "Larry Smith Jr."
__email___ = "mrlesmithjr@gmail.com"
__maintainer__ = "Larry Smith Jr."
__status__ = "Development"
# http://everythingshouldbevirtual.com
# @mrlesmithjr

class AnsibleMySQL(object):
    """
    Setup Main execution
    """

    def __init__(self):

        self.read_cli_args()

        if self.args.all:
            self.sql = """
                SELECT
                `inventory_hostname`,`ansible_ssh_host`,`ansible_distribution`,
                `ansible_distribution_release`,`ansible_distribution_version`,
                `group_names`
                FROM inventory"""
        elif self.args.allgroups:
            self.sql = """
                SELECT DISTINCT `group_names`
                FROM Groups"""
        elif self.args.allhosts:
            self.sql = """
                SELECT DISTINCT `inventory_hostname`
                FROM Hosts"""
        elif self.args.querygroup:
            self.sql = """
                SELECT `inventory_hostname`,`ansible_ssh_host`
                FROM inventory
                WHERE `group_names`='%s'
                ORDER BY `inventory_hostname`
                """ %(self.args.querygroup)
        elif self.args.queryhost:
            self.sql = """
                SELECT `inventory_hostname`,`ansible_ssh_host`,`group_names`
                FROM inventory
                WHERE `inventory_hostname`='%s'
                """ %(self.args.queryhost)
        elif self.args.queryhostdetails:
            self.sql = """
                SELECT *
                FROM HostDetails
                WHERE HostId IN
                (SELECT HostID FROM Hosts WHERE inventory_hostname = '%s')
                """ %(self.args.queryhostdetails)
        else:
            self.sql = """
                SELECT
                `inventory_hostname`,`ansible_ssh_host`,`ansible_distribution`,
                `ansible_distribution_release`,`ansible_distribution_version`,
                `group_names`
                FROM inventory"""

        self.gather_inventory()
        self.process_results()

    def gather_inventory(self):
        """
        Gather inventory from MySQL based on query
        """
        try:
            self.con = MySQLdb.connect(self.args.host, self.args.user,
                                       self.args.password, self.args.db)
            self.cur = self.con.cursor()
            self.cur.execute(self.sql)
            self.rows = self.cur.fetchall()
        finally:
            self.cur.close()
            self.con.close()

    def process_results(self):

        """
        Process and display results of the query
        """

        self.columns = [desc[0] for desc in self.cur.description]
        self.results = []
        for self.row in self.rows:
            self.row = dict(zip(self.columns, self.row))
            self.results.append(self.row)
        print json.dumps(self.results, sort_keys=True, default=datetime_handler)

    def read_cli_args(self):
        """
        Setup and Read Command Line Arguments to Pass
        """

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
        parser.add_argument('--queryhostdetails',
                            help='Query Host Full Details, Define Host to Query')
        parser.add_argument('--user', required=True, help='Database User')
        self.args = parser.parse_args()

def datetime_handler(obj):
    """
    JSON serializer for objects not serializable by default json code
    """
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Unknown type")

if __name__ == '__main__':
    AnsibleMySQL()
