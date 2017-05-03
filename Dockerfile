FROM mrlesmithjr/mysql

MAINTAINER Larry Smith Jr. <mrlesmithjr@gmail.com>

COPY ansible_tasks /opt/ansible_tasks

COPY library /opt

RUN ansible-galaxy install -r /opt/ansible_tasks/requirements.yml && \
    ansible-playbook -i "localhost," -c local /opt/ansible_tasks/playbook.yml
