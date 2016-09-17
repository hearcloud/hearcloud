#!/bin/bash
# Any subsequent(*) commands which fail will cause the shell script to exit immediately
set -e

ansible-playbook provision.yml --ask-sudo-pass --ask-vault-pass
fab -H mpvillafranca@hearcloud.com migrate
fab -H mpvillafranca@hearcloud.com config_nginx
fab -H mpvillafranca@hearcloud.com runserver 
