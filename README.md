## Demo
[![Everything Is AWESOME](https://i.imgur.com/AbSNncW.png)](https://vimeo.com/307816302)

## Set up
1. clone the repository
```
sudo apt-get install -y git
git clone https://a3e87b237eafce28b781a3834d8c1b103e748d6d@github.com/libbyandhelen/cuhk-timetable.git
cd cuhk-timetable/timetable
```

2. install django and its dependencies
```
sudo apt-get install -y python3-pip
python3 -m pip install --upgrade pip setuptools
sudo pip3 install django
sudo pip3 install django-haystack
sudo pip3 install Django-crontab
```

3. install and config mysql
```
sudo apt-get install -y mysql-server
mysql -u root -p
mysql> CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';
mysql> GRANT ALL PRIVILEGES ON * . * TO 'newuser'@'localhost';
mysql> FLUSH PRIVILEGES;
mysql> create database mydb;
```
```
sudo apt-get install -y libmysqlclient-dev
sudo pip3 install mysqlclient
Create mysql.local.conf
[client]
host = localhost
port = 3306
database = timetable
user = timetable
password = timetable
default-character-set = utf8
```

4. install and start elasticsearch
```
sudo add-apt-repository -y ppa:webupd8team/java
sudo apt-get update
sudo apt-get -y install oracle-java8-installer
wget -qO - https://packages.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
echo "deb http://packages.elastic.co/elasticsearch/1.7/debian stable main" | sudo tee -a /etc/apt/sources.list.d/elasticsearch-1.7.list
sudo apt-get update
sudo apt-get -y install elasticsearch
//sudo vi /etc/elasticsearch/elasticsearch.yml
//network.host: localhost
sudo service elasticsearch restart
sudo pip3 install elasticsearch
```
5. serve the website using nginx
```
sudo apt-get install -y python3-pip python3-dev libpq-dev nginx
sudo pip3 install gunicorn
sudo nano /etc/systemd/system/gunicorn.service
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=libby
Group=www-data
WorkingDirectory=/home/libby/Documents/cuhktimetable/timetable
ExecStart=/usr/local/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/libby/Documents/cuhktimetable/timetable/timetable.sock timetable.wsgi:application

[Install]
WantedBy=multi-user.target

sudo systemctl start gunicorn
sudo systemctl enable gunicorn

sudo nano /etc/nginx/sites-available/timetable
server {
    listen 80;
    server_name localhost;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/libby/Documents/cuhktimetable/timetable;
    }
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/home/libby/Documents/cuhktimetable/timetable/timetable.sock;
    }

}

Python3 manage.py collectstatic

sudo ln -s /etc/nginx/sites-available/timetable /etc/nginx/sites-enabled
sudo ufw allow 'Nginx Full'
```

6. run server
```
python3 manage.py migrate
python3 manage.py runserver localhost:8000
```

7. install scrapy
```
sudo pip3 install scrapy
sudo pip3 install pyasn1 --upgrade
```
8. setup scrapy job and crontab job
```
cd course_spider
sudo python3 setup.py install
change python path /usr/bin/python3
Change scrapy setting Django path /home/libby/Documents/cuhk-timetable/timetable
python3 manage.py crontab add
```
9. reindexing
```
python3.6 manage.py rebuild_index
```
9. run scrapy job manually (optional)
alphanums ranging from 0 to 25 for each alphabet respectively
```
cd course_spider/spider
scrapy crawl -a alphanums=0 course
```
