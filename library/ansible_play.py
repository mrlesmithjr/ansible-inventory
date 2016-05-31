#!/usr/bin/env python
"""
ansible_play.py: Ansible dynamic inventory

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

"""
Define vars
"""
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
    SELECT h.inventory_hostname, hv.VarName, hv.VarValue
    FROM
    Hosts as h,HostVars as hv
    WHERE h.HostId = hv.HostId
    """
SQL4 = """
    SELECT g.group_names, gv.VarName, gv.VarValue
    FROM
    Groups as g,GroupVars as gv
    WHERE g.GroupId = gv.GroupId
    """

class AnsibleMySQL(object):
    """
    Setup class for Ansible Dynamic Inventory
    """

    def __init__(self):
        """
        Init initial inventory
        """
        self.inventory = {}

        """
        Build out inventory structure
        """
        self.db_connect()
        self.db_query()
        self.group_list()
        self.group_vars()
        self.host_vars()
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
            self.cur.execute(SQL4)
            self.rows4 = self.cur.fetchall()
        finally:
            self.cur.close()
            self.con.close()

    def display_results(self):
        """
        Display final inventoy results
        """
        print json.dumps(self.inventory, default=datetime_handler, indent=2)

    def group_list(self):
        """
        Build inventory group list
        """
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

    def group_vars(self):
        """
        Gather group vars for each group
        """
        for self.row in range(len(self.rows4)):
            self.groups = (self.rows4[self.row][0])
            self.inventory[self.groups]['vars'] = {}
            for self.row4 in range(len(self.rows4)):
                self.group = self.rows4[self.row4][0]
                if self.group == self.groups:
                    self.var = self.rows4[self.row4][1]
                    self.val = self.rows4[self.row4][2]
                    self.inventory[self.group]['vars'][self.var] = self.val

    def host_vars(self):
        """
        Gather all inventory hostvars
        """
        self.inventory['_meta'] = {}
        self.inventory['_meta']['hostvars'] = {}
        for self.row in range(len(self.rows3)):
            self.hosts = self.rows3[self.row][0]
            self.ssh_host = self.rows3[self.row][1]
            self.inventory['_meta']['hostvars'][self.hosts] = {}
            for self.row3 in range(len(self.rows3)):
                self.host = self.rows3[self.row3][0]
                if self.host == self.hosts:
                    self.var = self.rows3[self.row3][1]
                    self.val = self.rows3[self.row3][2]
                    self.inventory['_meta']['hostvars'][self.host][self.var] = self.val

def datetime_handler(obj):
    """
    JSON serializer for objects not serializable by default json code
    """
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Unknown type")

if __name__ == '__main__':
    AnsibleMySQL()
