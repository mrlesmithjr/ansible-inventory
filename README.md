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
Using the included python script to execute quries.

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
                            --user USER

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
  --user USER           Database User
````
Default query...
````
ansible_inventory.py --user ansible --password ansible
````
````
[["node0", "172.28.128.21", "Ubuntu", "trusty", "14.04", "db-nodes"], ["node1", "172.28.128.22", "Ubuntu", "trusty", "14.04", "mixed-nodes"], ["node1", "172.28.128.22", "Ubuntu", "trusty", "14.04", "test-nodes"], ["node2", "172.28.128.23", "Ubuntu", "trusty", "14.04", "mixed-nodes"], ["node2", "172.28.128.23", "Ubuntu", "trusty", "14.04", "test-nodes"], ["node3", "172.28.128.24", "Ubuntu", "trusty", "14.04", "test-nodes"], ["node4", "172.28.128.25", "Ubuntu", "trusty", "14.04", "mixed-nodes"], ["node4", "172.28.128.25", "Ubuntu", "trusty", "14.04", "random-nodes"], ["node5", "172.28.128.26", "Ubuntu", "trusty", "14.04", "random-nodes"]]
````
Query all groups...
````
ansible_inventory.py --user ansible --password ansible --allgroups
````
````
[["db-nodes"], ["mixed-nodes"], ["random-nodes"], ["test-nodes"]]
````
Query all hosts...
````
ansible_inventory.py --user ansible --password ansible --allhosts
````
````
[["node0"], ["node1"], ["node2"], ["node3"], ["node4"], ["node5"], ["test2"], ["test5"], ["WTF"]]
````
Query a specific group...
````
ansible_inventory.py --user ansible --password ansible --querygroup test-nodes
````
````
[["node1", "172.28.128.22"], ["node2", "172.28.128.23"], ["node3", "172.28.128.24"]]
````
Query a specific host...
````
ansible_inventory.py --user ansible --password ansible --queryhost node1
````
````
[["node1", "172.28.128.22", "mixed-nodes"], ["node1", "172.28.128.22", "test-nodes"]]
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
