#!/usr/bin/bash
# Script to create database tables
# And seed data with location

cd /opt/api/app/db/

alembic upgrade head

python /opt/api/app/db/seed_db.py
