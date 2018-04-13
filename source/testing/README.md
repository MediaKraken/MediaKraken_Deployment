Audio test sounds provided by MediaCollege.com

coverage run xxxx.py

py.test --cov=test_database test_database/
from main dir......to grab all the source code
py.test --cov=. testing/test_database/
coverage report

pip pylint

sudo pip install -r pip_requirements.txt

# to build all the pip reqs
sudo apt-get install postgresql-server-dev-9.5 libsnmp-dev libldap2-dev libsasl2-dev python-dev libssl-dev libxml2-dev libxslt-dev



# setup postgresql user
sudo adduser metamanpg
sudo su - postgres
psql
CREATE USER metamanpg WITH PASSWORD 'metamanpg';
CREATE DATABASE metamandb OWNER metamanpg;
\q
exit


sudo nano /etc/postgresql/9.5/main/postgresql.conf
add "listen_addresses = '*'"
sudo nano /etc/postgresql/9.5/main/pg_hba.conf
# add host line for remote access
change local add all peer to md5 for backup login
sudo service postgresql restart

