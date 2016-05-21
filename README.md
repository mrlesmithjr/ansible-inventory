Role Name
=========

A brief description of the role goes here.

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

License
-------

BSD

Author Information
------------------

Larry Smith Jr.
- @mrlesmithjr
- http://everythingshouldbevirtual.com
- mrlesmithjr [at] gmail.com
