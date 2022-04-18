CREATE DATABASE mikenskietdb;
ALTER ROLE mikenkietdb_user SET client_encoding TO 'utf8';
ALTER ROLE mikenkietdb_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE mikenkietdb_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE mikenskietdb TO mikenkietdb_user;