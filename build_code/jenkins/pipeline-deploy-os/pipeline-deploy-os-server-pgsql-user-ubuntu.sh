#!/bin/bash
su - postgres
psql
CREATE USER metamanpg WITH PASSWORD 'metamanpg';
CREATE DATABASE metamandb OWNER metamanpg;
\q
exit
