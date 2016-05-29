#!/usr/bin/env python
"""
play.py: Ansible dynamic inventory

This script will query back-end MySQL DB
and generate a useable Ansible inventory
"""

#import argparse
import datetime
import json
import MySQLdb

__author__ = "Larry Smith Jr."
__email___ = "mrlesmithjr@gmail.com"
__maintainer__ = "Larry Smith Jr."
__status__ = "Development"
# http://everythingshouldbevirtual.com
# @mrlesmithjr

HOST = '127.0.0.1'
USER = 'ansible'
PASSWORD = 'ansible'
DB = 'ansible_inventory'
SQL = """
    SELECT hg.group_names, h.inventory_hostname, hd.ansible_ssh_host
    FROM
    HostGroups AS hg, Hosts AS h, HostDetails AS hd
    WHERE h.HostId = hd.HostId AND h.HostId = hg.HostId
    """
SQL2 = """
    SELECT group_names, inventory_hostname
    FROM
    HostGroups
    """
SQL3 = """
    SELECT DISTINCT h.inventory_hostname, hd.ansible_ssh_host
    FROM
    Hosts AS h, HostDetails AS hd
    WHERE h.HostId = hd.HostId
    """

class AnsibleMySQL(object):
    """
    Setup class for Ansible Dynamic Inventory
    """

    def __init__(self):
        self.db_connect()
        self.db_query()
        self.group_list()
#        self.group_list_test()
#        self.host_vars()
        self.display_results()

    def db_connect(self):
        """
        Setup MySQL DB connection
        """
        self.con = MySQLdb.connect(HOST, USER, PASSWORD, DB)
        self.cur = self.con.cursor()

    def db_query(self):
        """
        Query MySQL DB for each SQL Query
        """
        try:
            self.cur.execute(SQL)
            self.rows = self.cur.fetchall()
            self.cur.execute(SQL2)
            self.rows2 = self.cur.fetchall()
            self.cur.execute(SQL3)
            self.rows3 = self.cur.fetchall()
        finally:
            self.cur.close()
            self.con.close()

    def display_results(self):
        """
        Display final inventoy results
        """
        print json.dumps(self.inventory, default=datetime_handler, indent=2)

    def group_list_test(self):
        """
        Test - This is for testing new functions

        Build inventory group list
        """
        self.inventory = {}
        self.columns = [desc[0] for desc in self.cur.description]
        for self.row in range(len(self.rows)):
            self.hosts = list()
            self.group = (self.rows[self.row][0])
            self.host = (self.rows[self.row][1])
            for self.row2 in range(len(self.rows2)):
                """
                Gather and compare group names in order to find hosts within
                the group and build the hosts correctly.
                """
                self.group2 = (self.rows2[self.row2][0])
                self.host2 = (self.rows2[self.row2][1])
                self.hostvars = {}
                if self.group2 == self.group:
                    self.hosts.append(self.host2)
                    self.inventory[self.group] = {
                        'hosts': self.hosts,
                    }

    def group_list(self):
        """
        Build inventory group list
        """
        self.inventory = {}
        self.columns = [desc[0] for desc in self.cur.description]
        for self.row in range(len(self.rows)):
            self.hosts = list()
            self.group = (self.rows[self.row][0])
            self.host = (self.rows[self.row][1])
            for self.row2 in range(len(self.rows2)):
                """
                Gather and compare group names in order to find hosts within
                the group and build the hosts correctly.
                """
                self.group2 = (self.rows2[self.row2][0])
                self.host2 = (self.rows2[self.row2][1])
                self.hostvars = {}
                if self.group2 == self.group:
                    self.hosts.append(self.host2)
                    self.inventory[self.group] = {
                        'hosts': self.hosts,
                    }

    def host_vars(self):
        """
        Gather all inventory hostvars
        """
        self.inventory['_meta'] = {}
        self.inventory['_meta']['hostvars'] = list()
        for self.row3 in range(len(self.rows3)):
            self.host = (self.rows3[self.row3][0])
            self.ssh_host = (self.rows3[self.row3][1])
            self.key = {
                self.host:
                {'ansible_ssh_host': self.ssh_host},
            }
            self.inventory['_meta']['hostvars'].append(self.key)

def datetime_handler(obj):
    """
    JSON serializer for objects not serializable by default json code
    """
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Unknown type")

if __name__ == '__main__':
    AnsibleMySQL()
