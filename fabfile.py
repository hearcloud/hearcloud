from fabric.api import run
from fabric.context_managers import cd

def migrate():
    run('cd /home/mpvillafranca/hearcloud && source /home/mpvillafranca/VirtualEnvs/hcenv/bin/activate && python manage.py migrate')

def checkout_dev():
    with cd('/home/mpvillafranca/hearcloud'):
        run('git checkout dev')
        run('git pull')

def checkout_master():
    with cd('/home/mpvillafranca/hearcloud'):
        run('git checkout master')
        run('git pull')

def config_nginx():
    with cd('/home/mpvillafranca/hearcloud'):
        run('source /home/mpvillafranca/VirtualEnvs/hcenv/bin/activate && python manage.py collectstatic')
        run ('cd production-webconfig && python supervisor.conf')
        run('sudo cp production-webconfig/default /etc/nginx/sites-available/')
        run('sudo cp production-webconfig/nginx.conf /etc/nginx/')
        run('sudo cp production-webconfig/supervisor.conf /etc/supervisor/conf.d/')

def runserver():
    run('sudo service nginx restart')
    run('sudo service supervisor restart')
