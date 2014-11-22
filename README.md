# Setup on Arch Linux


packages to install:
```
#!text
python-django
uwsgi
uwsgi-plugin-python
nginx
```

repo setup:
```
#!text
cd
mkdir drs
cd drs
git init
git remote add origin git@bitbucket.org:afg984/dit-robotics-site.git
git pull origin master
```

uwsgi setup:

change pid to afg in /etc/uwsgi/emperor.ini
```
#!text
sudo systemctl enable emperor.uwsgi
sudo mkdir /etc/uwsgi/vassals
sudo ln -s /home/afg/drs/drs_uwsgi.ini /etc/uwsgi/vassals/
```

nginx setup:

remove "location /" block in /etc/nginx/nginx.conf
```
#!text
sudo systemctl enable nginx
sudo mkdir /etc/nginx/sites-enabled
sudo ln -s /home/afg/drs/drs_nginx.conf /etc/nginx/sites-enabled/
```
