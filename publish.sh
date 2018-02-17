cd /data/wjvr
sudo git pull
sudo python manage.py collectstatic --noinput
sudo python manage.py compress
sudo python manage.py migrate
sudo touch /data/wjvr/uwsgi.ini
