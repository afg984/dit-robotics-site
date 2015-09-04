# Setup on Arch Linux

This is just a note for reinstallation

###Packages Required
```
python >= 3.4
uwsgi
uwsgi-plugin-python
nginx
postgresql
```

###Repository Setup

The user "http" must have access to the project directory.


###Drive Setup
```
mkdir media
chmod 775 media
```

###uWSGI Setup
```
sudo systemctl enable emperor.uwsgi
sudo mkdir /etc/uwsgi/vassals
sudo ln -s /home/dit/drs/drs_uwsgi.ini /etc/uwsgi/vassals/
```

###Nginx Setup

in /etc/nginx/nginx.conf:

add "user http http;"

remove "location /" block
```
sudo systemctl enable nginx
sudo mkdir /etc/nginx/sites-enabled
sudo ln -s /home/dit/drs/drs_nginx.conf /etc/nginx/sites-enabled/
```
