# Setup on Arch Linux


###Packages Required
```
#!text
python-django
uwsgi
uwsgi-plugin-python
nginx
python-beautifulsoup4
```

###Repository Setup

The user "http" must have access to the project directory.

This is currently achieved by adding "http" to "afg" group.
```
#!text
cd
mkdir drs
cd drs
git init
git remote add origin git@bitbucket.org:afg984/dit-robotics-site.git
git pull origin master
```

###uWSGI Setup
```
#!text
sudo systemctl enable emperor.uwsgi
sudo mkdir /etc/uwsgi/vassals
sudo ln -s /home/afg/drs/drs_uwsgi.ini /etc/uwsgi/vassals/
```

###Nginx Setup

in /etc/nginx/nginx.conf:

add "user http http;"

remove "location /" block
```
#!text
sudo systemctl enable nginx
sudo mkdir /etc/nginx/sites-enabled
sudo ln -s /home/afg/drs/drs_nginx.conf /etc/nginx/sites-enabled/
```