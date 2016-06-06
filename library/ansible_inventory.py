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
        self.process_cli_args()
        self.gather_inventory()
        self.process_results()

    def gather_inventory(self):
        """
        Gather inventory from MySQL based on query
        """
        try:
            self.con = MySQLdb.connect(self.args.dbhost, self.args.dbuser,
                                       self.args.dbpassword, self.args.dbname)
            self.cur = self.con.cursor()
            self.cur.execute(self.sql)
            self.rows = self.cur.fetchall()
        finally:
            self.cur.close()
            self.con.close()

    def process_cli_args(self):
        """
        Process command-line cli arguments passed
        """
        if self.args.action == "queryall":
            self.sql = """
                SELECT h.inventory_hostname, hg.group_names, hd.*
                FROM
                HostDetails AS hd, Hosts AS h, HostGroups AS hg
                WHERE h.HostId = hd.HostId AND h.HostId = hg.HostId
                ORDER BY h.inventory_hostname
                """
        elif self.args.action == "queryallgroups":
            self.sql = """
                SELECT DISTINCT `group_names`
                FROM Groups
                ORDER BY group_names
                """
        elif self.args.action == "queryallhosts":
            self.sql = """
                SELECT DISTINCT `inventory_hostname`
                FROM Hosts
                ORDER BY inventory_hostname
                """
        elif self.args.action == "querygroup":
            self.sql = """
                SELECT hg.group_names, h.inventory_hostname, hd.ansible_hostname, hd.ansible_ssh_host
                FROM
                HostDetails AS hd, Hosts AS h, HostGroups AS hg
                WHERE h.HostId = hd.HostId AND h.HostId = hg.HostId AND hg.group_names = "%s"
                ORDER BY h.inventory_hostname
                """ %(self.args.group)
        elif self.args.action == "queryhost":
            self.sql = """
                SELECT h.inventory_hostname, hd.ansible_hostname, hd.ansible_ssh_host, hg.group_names
                FROM
                HostDetails AS hd, Hosts AS h, HostGroups AS hg
                WHERE h.HostId = hd.HostId AND h.HostId = hg.HostId AND h.inventory_hostname = "%s"
                ORDER BY hg.group_names
                """ %(self.args.host)
        elif self.args.action == "queryhostdetails":
            self.sql = """
                SELECT *
                FROM HostDetails
                WHERE HostId IN
                (SELECT HostID FROM Hosts WHERE inventory_hostname = '%s')
                """ %(self.args.host)
        else:
            self.sql = """
                SELECT h.inventory_hostname, hg.group_names, hd.*
                FROM
                HostDetails AS hd, Hosts AS h, HostGroups AS hg
                WHERE h.HostId = hd.HostId AND h.HostId = hg.HostId
                """

    def process_results(self):
        """
        Process and display results of the query
        """
        self.columns = [desc[0] for desc in self.cur.description]
        self.results = []
        for self.row in self.rows:
            self.row = dict(zip(self.columns, self.row))
            self.results.append(self.row)
        print json.dumps(self.results, default=datetime_handler, indent=4)

    def read_cli_args(self):
        """
        Setup and Read Command Line Arguments to Pass
        """
        parser = argparse.ArgumentParser(description='Ansible Inventory...')
        parser.add_argument('action', help='Define action to take',
                            choices=['queryall', 'queryallgroups', 'queryallhosts',
                                     'querygroup', 'queryhost', 'queryhostdetails'])
        parser.add_argument('--dbhost', default='127.0.0.1',
                            help='Database Host, [default: 127.0.0.1]')
        parser.add_argument('--dbname', default='ansible_inventory',
                            help='Database Name, [default: ansible_inventory]')
        parser.add_argument('--dbpassword', required=True,
                            help='Database Password')
        parser.add_argument('--dbuser', required=True, help='Database User')
        parser.add_argument('--group', help='Query Group, Define Group to Query')
        parser.add_argument('--host', help='Query Host, Define Host to Query')
        self.args = parser.parse_args()
        if (self.args.action == "queryhost" or
                self.args.action == "queryhostdetails") and self.args.host is None:
            parser.error("--host is required")
        if self.args.action == "querygroup" and self.args.group is None:
            parser.error("--group is required")

def datetime_handler(obj):
    """
    JSON serializer for objects not serializable by default json code
    """
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Unknown type")

if __name__ == '__main__':
    AnsibleMySQL()
