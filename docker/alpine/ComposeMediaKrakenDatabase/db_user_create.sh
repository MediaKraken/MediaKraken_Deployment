# as root
/etc/init.d/postgresql start
su postgres
# create db for metaman
psql
CREATE USER metamanpg WITH PASSWORD 'metamanpg';
CREATE DATABASE metamandb OWNER metamanpg;
\q

exit
