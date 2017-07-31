#!/bin/sh
su postgres
psql -d metamandb -c "create extension pg_trgm;"
\q
