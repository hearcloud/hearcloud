ansible-playbook provision.yml --ask-sudo-pass
fab -H mpvillafranca@hearcloud.com migrate
fab -H mpvillafranca@hearcloud.com checkout_dev
fab -H mpvillafranca@hearcloud.com config_nginx
fab -H mpvillafranca@hearcloud.com runserver 
