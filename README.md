Role Name
=========

An Ansible role to deploy an Ansible Inventory system using MySQL as the back-end.  

Intentions
----------
The intention of this role is to build a dynamic inventory system by leveraging  
Ansible gathered facts and storing those in the MySQL DB. This inventory system  
can be extended to provide for example...
- A dynamic inventory for Ansible
- Ability to drive additional tasks
  - Run Ansible playbooks based on hosts/groups and etc.
  - Become and Ansible module for manipulating data in MySQL (instead of raw shell commands)
  - Tie into CI/CD tools for integrations
  - Tie into logging systems (ELK) directly
  - Tie into Maintenance scheduling and notifications
  - Many other abilities

So think of this as a building block for something potentially bigger than  
collecting a bunch of Ansible facts. But giving the ability to tenants/users  
to take actions based on this collection of data.  

Does this make sense? Maybe, maybe not. I have a lot of thoughts in mind for  
this. But it may not make any sense to pursue. Time will tell. I am of course  
open to any input and contributions.  

My additional thought is to wrap possibly Django around the front-end.

Requirements
------------

Install required Ansible roles...  
````
ansible-galaxy install -r requirements.yml
````

Role Variables
--------------

````
---
# defaults file for ansible-inventory
inventory_db_name: 'ansible_inventory'  #Define the Inventory DB Name
inventory_db_host: 'node0'  #Define the inventory_hostname in which the Inventory DB is to reside
````

Dependencies
------------

None

Example Playbook
----------------
````
- hosts: db-nodes
  become: true
  vars:
    - mysql_allow_remote_connections: true
    - mysql_root_password: root
    - pri_domain_name: 'test.vagrant.local'
  roles:
    - role: ansible-apache2
    - role: ansible-mariadb-mysql
  tasks:

- hosts: all
  become: true
  vars:
    - pri_domain_name: 'test.vagrant.local'
  roles:
    - role: ansible-inventory
  tasks:
````

Example Queries
---------------
Using the included python script to execute queries. (In all of the example
  outputs I am using jq to show pretty JSON.)

````
library/ansible_inventory.py
````

Show script help..
````
ansible_inventory.py -h
````
````
usage: ansible_inventory.py [-h] [--all] [--allgroups] [--allhosts] [--db DB]
                            [--host HOST] --password PASSWORD
                            [--querygroup QUERYGROUP] [--queryhost QUERYHOST]
                            [--queryhostdetails QUERYHOSTDETAILS] --user USER

Ansible Inventory...

optional arguments:
  -h, --help            show this help message and exit
  --all                 Display all inventory items
  --allgroups           Display all groups
  --allhosts            Display all hosts
  --db DB               Database Name
  --host HOST           Database Host, [default: 127.0.0.1]
  --password PASSWORD   Database Password
  --querygroup QUERYGROUP
                        Query Group, Define Group to Query
  --queryhost QUERYHOST
                        Query Host, Define Host to Query
  --queryhostdetails QUERYHOSTDETAILS
                        Query Host Full Details, Define Host to Query
  --user USER           Database User
````
Default query...
````
ansible_inventory.py --user ansible --password ansible | jq
````
````
[
  {
    "HostDetailsId": 1,
    "HostId": 1,
    "LastUpdateTime": "2016-05-25T18:01:07",
    "ansible_architecture": "x86_64",
    "ansible_bios_date": "12/01/2006",
    "ansible_bios_version": "VirtualBox",
    "ansible_date_time.tz": "EDT",
    "ansible_default_ipv4.address": "10.0.2.15",
    "ansible_default_ipv4.gateway": "10.0.2.2",
    "ansible_default_ipv4.interface": "eth0",
    "ansible_default_ipv4.macaddress": "08:00:27:55:7c:f9",
    "ansible_default_ipv4.netmask": "255.255.255.0",
    "ansible_distribution": "Ubuntu",
    "ansible_distribution_release": "trusty",
    "ansible_distribution_version": "14.04",
    "ansible_fqdn": "node0",
    "ansible_hostname": "node0",
    "ansible_kernel": "4.2.0-30-generic",
    "ansible_memfree_mb": 108,
    "ansible_memtotal_mb": 489,
    "ansible_nodename": "node0",
    "ansible_os_family": "Debian",
    "ansible_processor": "GenuineIntelIntel(R) Core(TM) i7-4870HQ CPU @ 2.50GHz",
    "ansible_processor_cores": 1,
    "ansible_processor_count": 1,
    "ansible_product_name": "VirtualBox",
    "ansible_ssh_host": "172.28.128.60",
    "ansible_swapfree_mb": 502,
    "ansible_swaptotal_mb": 511,
    "ansible_system_vendor": "innotek GmbH",
    "ansible_virtualization_type": "virtualbox",
    "group_names": "db-nodes",
    "inventory_hostname": "node0"
  },
  {
    "HostDetailsId": 2,
    "HostId": 2,
    "LastUpdateTime": "2016-05-25T18:01:07",
    "ansible_architecture": "x86_64",
    "ansible_bios_date": "12/01/2006",
    "ansible_bios_version": "VirtualBox",
    "ansible_date_time.tz": "EDT",
    "ansible_default_ipv4.address": "10.0.2.15",
    "ansible_default_ipv4.gateway": "10.0.2.2",
    "ansible_default_ipv4.interface": "eth0",
    "ansible_default_ipv4.macaddress": "08:00:27:a0:a8:23",
    "ansible_default_ipv4.netmask": "255.255.255.0",
    "ansible_distribution": "Debian",
    "ansible_distribution_release": "jessie",
    "ansible_distribution_version": "8.3",
    "ansible_fqdn": "node1",
    "ansible_hostname": "node1",
    "ansible_kernel": "3.16.0-4-amd64",
    "ansible_memfree_mb": 78,
    "ansible_memtotal_mb": 494,
    "ansible_nodename": "node1",
    "ansible_os_family": "Debian",
    "ansible_processor": "GenuineIntelIntel(R) Core(TM) i7-4870HQ CPU @ 2.50GHz",
    "ansible_processor_cores": 1,
    "ansible_processor_count": 1,
    "ansible_product_name": "VirtualBox",
    "ansible_ssh_host": "172.28.128.56",
    "ansible_swapfree_mb": 1020,
    "ansible_swaptotal_mb": 1020,
    "ansible_system_vendor": "innotek GmbH",
    "ansible_virtualization_type": "virtualbox",
    "group_names": "mixed-nodes",
    "inventory_hostname": "node1"
  },
  {
    "HostDetailsId": 2,
    "HostId": 2,
    "LastUpdateTime": "2016-05-25T18:01:07",
    "ansible_architecture": "x86_64",
    "ansible_bios_date": "12/01/2006",
    "ansible_bios_version": "VirtualBox",
    "ansible_date_time.tz": "EDT",
    "ansible_default_ipv4.address": "10.0.2.15",
    "ansible_default_ipv4.gateway": "10.0.2.2",
    "ansible_default_ipv4.interface": "eth0",
    "ansible_default_ipv4.macaddress": "08:00:27:a0:a8:23",
    "ansible_default_ipv4.netmask": "255.255.255.0",
    "ansible_distribution": "Debian",
    "ansible_distribution_release": "jessie",
    "ansible_distribution_version": "8.3",
    "ansible_fqdn": "node1",
    "ansible_hostname": "node1",
    "ansible_kernel": "3.16.0-4-amd64",
    "ansible_memfree_mb": 78,
    "ansible_memtotal_mb": 494,
    "ansible_nodename": "node1",
    "ansible_os_family": "Debian",
    "ansible_processor": "GenuineIntelIntel(R) Core(TM) i7-4870HQ CPU @ 2.50GHz",
    "ansible_processor_cores": 1,
    "ansible_processor_count": 1,
    "ansible_product_name": "VirtualBox",
    "ansible_ssh_host": "172.28.128.56",
    "ansible_swapfree_mb": 1020,
    "ansible_swaptotal_mb": 1020,
    "ansible_system_vendor": "innotek GmbH",
    "ansible_virtualization_type": "virtualbox",
    "group_names": "test-nodes",
    "inventory_hostname": "node1"
  },
  {
    "HostDetailsId": 3,
    "HostId": 3,
    "LastUpdateTime": "2016-05-25T18:01:07",
    "ansible_architecture": "x86_64",
    "ansible_bios_date": "12/01/2006",
    "ansible_bios_version": "VirtualBox",
    "ansible_date_time.tz": "EDT",
    "ansible_default_ipv4.address": "10.0.2.15",
    "ansible_default_ipv4.gateway": "10.0.2.2",
    "ansible_default_ipv4.interface": "eth0",
    "ansible_default_ipv4.macaddress": "08:00:27:55:7c:f9",
    "ansible_default_ipv4.netmask": "255.255.255.0",
    "ansible_distribution": "Ubuntu",
    "ansible_distribution_release": "trusty",
    "ansible_distribution_version": "14.04",
    "ansible_fqdn": "node2",
    "ansible_hostname": "node2",
    "ansible_kernel": "4.2.0-30-generic",
    "ansible_memfree_mb": 79,
    "ansible_memtotal_mb": 489,
    "ansible_nodename": "node2",
    "ansible_os_family": "Debian",
    "ansible_processor": "GenuineIntelIntel(R) Core(TM) i7-4870HQ CPU @ 2.50GHz",
    "ansible_processor_cores": 1,
    "ansible_processor_count": 1,
    "ansible_product_name": "VirtualBox",
    "ansible_ssh_host": "172.28.128.57",
    "ansible_swapfree_mb": 510,
    "ansible_swaptotal_mb": 511,
    "ansible_system_vendor": "innotek GmbH",
    "ansible_virtualization_type": "virtualbox",
    "group_names": "mixed-nodes",
    "inventory_hostname": "node2"
  },
  {
    "HostDetailsId": 3,
    "HostId": 3,
    "LastUpdateTime": "2016-05-25T18:01:07",
    "ansible_architecture": "x86_64",
    "ansible_bios_date": "12/01/2006",
    "ansible_bios_version": "VirtualBox",
    "ansible_date_time.tz": "EDT",
    "ansible_default_ipv4.address": "10.0.2.15",
    "ansible_default_ipv4.gateway": "10.0.2.2",
    "ansible_default_ipv4.interface": "eth0",
    "ansible_default_ipv4.macaddress": "08:00:27:55:7c:f9",
    "ansible_default_ipv4.netmask": "255.255.255.0",
    "ansible_distribution": "Ubuntu",
    "ansible_distribution_release": "trusty",
    "ansible_distribution_version": "14.04",
    "ansible_fqdn": "node2",
    "ansible_hostname": "node2",
    "ansible_kernel": "4.2.0-30-generic",
    "ansible_memfree_mb": 79,
    "ansible_memtotal_mb": 489,
    "ansible_nodename": "node2",
    "ansible_os_family": "Debian",
    "ansible_processor": "GenuineIntelIntel(R) Core(TM) i7-4870HQ CPU @ 2.50GHz",
    "ansible_processor_cores": 1,
    "ansible_processor_count": 1,
    "ansible_product_name": "VirtualBox",
    "ansible_ssh_host": "172.28.128.57",
    "ansible_swapfree_mb": 510,
    "ansible_swaptotal_mb": 511,
    "ansible_system_vendor": "innotek GmbH",
    "ansible_virtualization_type": "virtualbox",
    "group_names": "test-nodes",
    "inventory_hostname": "node2"
  },
  {
    "HostDetailsId": 5,
    "HostId": 5,
    "LastUpdateTime": "2016-05-25T18:01:07",
    "ansible_architecture": "x86_64",
    "ansible_bios_date": "12/01/2006",
    "ansible_bios_version": "VirtualBox",
    "ansible_date_time.tz": "EDT",
    "ansible_default_ipv4.address": "10.0.2.15",
    "ansible_default_ipv4.gateway": "10.0.2.2",
    "ansible_default_ipv4.interface": "enp0s3",
    "ansible_default_ipv4.macaddress": "08:00:27:af:3a:e6",
    "ansible_default_ipv4.netmask": "255.255.255.0",
    "ansible_distribution": "CentOS",
    "ansible_distribution_release": "Core",
    "ansible_distribution_version": "7.2.1511",
    "ansible_fqdn": "localhost.localdomain",
    "ansible_hostname": "node3",
    "ansible_kernel": "3.10.0-327.13.1.el7.x86_64",
    "ansible_memfree_mb": 403,
    "ansible_memtotal_mb": 992,
    "ansible_nodename": "node3",
    "ansible_os_family": "RedHat",
    "ansible_processor": "GenuineIntelIntel(R) Core(TM) i7-4870HQ CPU @ 2.50GHzGenuineIntelIntel(R) Core(TM) i7-4870HQ CPU @ 2.50GHz",
    "ansible_processor_cores": 2,
    "ansible_processor_count": 1,
    "ansible_product_name": "VirtualBox",
    "ansible_ssh_host": "172.28.128.58",
    "ansible_swapfree_mb": 1023,
    "ansible_swaptotal_mb": 1023,
    "ansible_system_vendor": "innotek GmbH",
    "ansible_virtualization_type": "virtualbox",
    "group_names": "test-nodes",
    "inventory_hostname": "node3"
  }
]
````
Query all groups...
````
ansible_inventory.py --user ansible --password ansible --allgroups | jq
````
````
[
  {
    "group_names": "db-nodes"
  },
  {
    "group_names": "mixed-nodes"
  },
  {
    "group_names": "random-nodes"
  },
  {
    "group_names": "test-nodes"
  }
]
````
Query all hosts...
````
ansible_inventory.py --user ansible --password ansible --allhosts | jq
````
````
[
  {
    "inventory_hostname": "node0"
  },
  {
    "inventory_hostname": "node1"
  },
  {
    "inventory_hostname": "node2"
  },
  {
    "inventory_hostname": "node3"
  },
  {
    "inventory_hostname": "node4"
  }
]
````
Query a specific group...
````
ansible_inventory.py --user ansible --password ansible --querygroup test-nodes | jq
````
````
[
  {
    "ansible_hostname": "node1",
    "ansible_ssh_host": "172.28.128.56",
    "group_names": "test-nodes",
    "inventory_hostname": "node1"
  },
  {
    "ansible_hostname": "node2",
    "ansible_ssh_host": "172.28.128.57",
    "group_names": "test-nodes",
    "inventory_hostname": "node2"
  },
  {
    "ansible_hostname": "node3",
    "ansible_ssh_host": "172.28.128.58",
    "group_names": "test-nodes",
    "inventory_hostname": "node3"
  }
]
````
Query a specific host...
````
ansible_inventory.py --user ansible --password ansible --queryhost node1 | jq
````
````
[
  {
    "ansible_hostname": "node1",
    "ansible_ssh_host": "172.28.128.56",
    "group_names": "mixed-nodes",
    "inventory_hostname": "node1"
  },
  {
    "ansible_hostname": "node1",
    "ansible_ssh_host": "172.28.128.56",
    "group_names": "test-nodes",
    "inventory_hostname": "node1"
  }
]
````
Query a specific host for all details...
````
ansible_inventory.py --user ansible --password ansible --queryhostdetails node1 | jq
````
````
[
  {
    "HostDetailsId": 2,
    "HostId": 2,
    "LastUpdateTime": "2016-05-25T18:01:07",
    "ansible_architecture": "x86_64",
    "ansible_bios_date": "12/01/2006",
    "ansible_bios_version": "VirtualBox",
    "ansible_date_time.tz": "EDT",
    "ansible_default_ipv4.address": "10.0.2.15",
    "ansible_default_ipv4.gateway": "10.0.2.2",
    "ansible_default_ipv4.interface": "eth0",
    "ansible_default_ipv4.macaddress": "08:00:27:a0:a8:23",
    "ansible_default_ipv4.netmask": "255.255.255.0",
    "ansible_distribution": "Debian",
    "ansible_distribution_release": "jessie",
    "ansible_distribution_version": "8.3",
    "ansible_fqdn": "node1",
    "ansible_hostname": "node1",
    "ansible_kernel": "3.16.0-4-amd64",
    "ansible_memfree_mb": 78,
    "ansible_memtotal_mb": 494,
    "ansible_nodename": "node1",
    "ansible_os_family": "Debian",
    "ansible_processor": "GenuineIntelIntel(R) Core(TM) i7-4870HQ CPU @ 2.50GHz",
    "ansible_processor_cores": 1,
    "ansible_processor_count": 1,
    "ansible_product_name": "VirtualBox",
    "ansible_ssh_host": "172.28.128.56",
    "ansible_swapfree_mb": 1020,
    "ansible_swaptotal_mb": 1020,
    "ansible_system_vendor": "innotek GmbH",
    "ansible_virtualization_type": "virtualbox"
  }
]
````

License
-------

BSD

Author Information
------------------

Larry Smith Jr.
- @mrlesmithjr
- http://everythingshouldbevirtual.com
- mrlesmithjr [at] gmail.com
