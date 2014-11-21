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
```
#!text
sudo systemctl enable emperor.uwsgi
sudo mkdir /etc/uwsgi/vassals
sudo ln -s /home/afg/drs/drs_uwsgi.ini /etc/uwsgi/vassals/
```

nginx setup:
```
#!text
sudo systemctl enable nginx
sudo ln -s /home/afg/drs/drs_nginx.conf /etc/nginx/sites-enabled
```