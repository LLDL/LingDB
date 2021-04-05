# Configuration

This guide assumes CentOS 8, and a sudoer user named admin

## Yum, mod_wsgi, and Apache:

Based on [Installing Apache on Centos 7](https://www.digitalocean.com/community/tutorials/how-to-install-the-apache-web-server-on-centos-7) and [mod_wsgi's install guide](https://modwsgi.readthedocs.io/en/develop/user-guides/quick-installation-guide.html).

```bash
sudo yum -y install httpd httpd-devel.x86_64 python36 python36-devel gcc make redhat-rpm-config git postgresql-server

sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
sudo systemctl enable httpd
sudo systemctl start httpd

cd ~
wget https://github.com/GrahamDumpleton/mod_wsgi/archive/refs/tags/4.7.1.tar.gz
tar xvfz 4.7.1.tar.gz
cd mod_wsgi-4.7.1
./configure --with-apxs=/usr/bin/apxs --with-python=/usr/bin/python3

make
sudo make install


cd ~/mod_wsgi-4.7.1
make clean
cd ~
rm -r mod_wsgi-4.7.1

sudo nano /etc/httpd/conf/httpd.conf
``` 

Following the instructions [here](https://modwsgi.readthedocs.io/en/develop/user-guides/quick-installation-guide.html#loading-module-into-apache), we will insert a line into `/etc/httpd/conf/httpd.conf`  right below the line `Include conf.modules.d/*.conf`: 
```
LoadModule wsgi_module modules/mod_wsgi.so
```

```bash
sudo nano /etc/services
```

Based on [this tutorial on ports](https://www.thegeekdiary.com/how-to-open-a-ports-in-centos-rhel-7/) allow port 8000 by inserting the following at the bottom of /etc/services (requires sudo):


```
django-test     8000/tcp                # ankit-test
django-test     8000/udp                # ankit-test
```

Then, proceed to make changes to the firewall: 

```
sudo firewall-cmd --zone=public --add-port=8000/tcp --permanent
sudo firewall-cmd --zone=public --add-port=8000/udp --permanent
sudo firewall-cmd --reload
```

## PostgreSQL

Based loosely on [this tutorial](https://www.redhat.com/en/blog/setting-django-application-rhel-8-beta)

```
sudo /usr/bin/postgresql-setup --initdb
systemctl enable --now postgresql
sudo -u postgres psql
create database participant_db;
create user pgadmin with password 'thisisabadpassword';
alter role pgadmin set client_encoding to 'utf8';
alter role pgadmin set default_transaction_isolation to 'read committed';
alter role pgadmin set timezone to 'utc';
grant all on DATABASE participant_db to pgadmin;
\q
```
Now, we must modify `/var/lib/pgsql/data/pg_hba.conf`
```bash
sudo nano /var/lib/pgsql/data/pg_hba.conf
```
Replace the IPv4 local and IPv6 local with:
```
# IPv4 local connections:
host    all        all 0.0.0.0/0                md5
# IPv6 local connections:
host    all        all ::1/128                 md5
```

Then, restart the postgres service:
```bash
sudo systemctl restart postgresql.service
```

## Permissions

Our django application will live in `/var/www/LingDB`, Python dependencies will be contained within a virtual environment, and the folder will have RWX enabled for a new group containing the admin and apache users. As well, we will set SELinux to log instead of enforce (this was the root of the issue).

```bash
sudo mkdir /var/www/LingDB
sudo setenforce 0
sudo groupadd djangousers
sudo gpasswd -a apache djangousers
sudo gpasswd -a admin djangousers
sudo chown -R admin:djangousers /var/www/LingDB
sudo chmod -R u+rwx /var/www/LingDB
```

The following may work if we simply do `sudo chmod -R g+rx /var/www/LingDB` but if that doesn't work, this may be necessary:
```bash
sudo chmod -R g+rwx /var/www/LingDB
```

## Django

Now, we will configure our Django app:

```
cd /var/www/LingDB
git clone https://github.com/LLDL/LingDB.git
mv /var/www/LingDB/LingDB/lingdb /var/www/LingDB
rm -r -f /var/www/LingDB/LingDB
cd /var/www/LingDB
python3 -m venv venv
source venv/bin/activate
cd lingdb
pip install -r requirements.txt
```

In the settingsSensitive file, update the secret key and database values as previously set in psql.

```
python3 manage.py makemigrations --settings=lingdb.settings.settingsSensitive
python3 manage.py migrate --settings=lingdb.settings.settingsSensitive
python3 manage.py createsuperuser 
python3 manage.py runserver --settings=lingdb.settings.settingsSensitive 0.0.0.0:8000
```
The application should be available at port 8000. To test static files, do the following:
```
pip install waitress
python manage.py collectstatic
waitress-serve --host=0.0.0.0 --port=8000 lingdb.wsgi:application
```
The webpage should load with the static files (images, css, js) without complaint, if that's the case, kill the server with ctrl+c and proceed. 

Last step, fingers crossed: plug the app into Apache using [the mod_wsgi tutorial](https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/modwsgi/)



```
sudo nano /etc/httpd/conf/httpd.conf
```

Append to `/etc/httpd/conf/httpd.conf`:
```

WSGIScriptAlias / /var/www/LingDB/lingdb/lingdb/wsgi.py
WSGIPythonHome /var/www/LingDB/venv
WSGIPythonPath /var/www/LingDB/lingdb


<Directory /var/www/LingDB/lingdb/lingdb>
<Files wsgi.py>
Require all granted
</Files> 
</Directory>

```

Then, restart apache:
```
sudo systemctl restart httpd
```