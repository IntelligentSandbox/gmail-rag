#!/bin/bash
sudo -u postgres psql -c "DROP DATABASE IF EXISTS emaildb;"
sudo -u postgres psql -c "DROP USER IF EXISTS emailuser;"
sudo -u postgres psql -c "CREATE DATABASE emaildb;"
sudo -u postgres psql -c "CREATE USER emailuser WITH PASSWORD 'emailpass';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE emaildb TO emailuser;"
sudo -u postgres psql -c "ALTER USER emailuser CREATEDB;"
sudo -u postgres psql -d emaildb -c "CREATE EXTENSION IF NOT EXISTS vector;"
sudo -u postgres psql -d emaildb -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO emailuser;"
sudo -u postgres psql -d emaildb -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO emailuser;"
sudo -u postgres psql -d emaildb -c "GRANT CREATE ON SCHEMA public TO emailuser;"
echo "DATABASE_URL=postgresql://emailuser:emailpass@localhost/emaildb" | tee .env
