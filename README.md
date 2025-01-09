# Stewardly

# Getting Started

First clone the repository from GitLab and switch to the new directory:

    $ git clone https://gitlab.com/stewardly/stewardly.git
    $ cd stewardly/backend/stewardly
    
# Requirements  

1. Install [Python 3.10](https://computingforgeeks.com/how-to-install-python-on-ubuntu-linux-system/)

2. Install Pip for Python3.10
```
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
```
3. Install virtual env for Python3.10:
```
python3 -m pip install virtualenv
virtualenv venv -p python3
```

4. [PostgreSQL](https://www.cherryservers.com/blog/how-to-install-and-setup-postgresql-server-on-ubuntu-20-04)
```
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get -y install postgresql

```
## Configure PostgreSQL

```
sudo -u postgres psql
CREATE DATABASE stewardly;
CREATE USER usr WITH PASSWORD '1234';
ALTER ROLE usr SET client_encoding TO 'utf8';
ALTER ROLE usr SET default_transaction_isolation TO 'read committed';
ALTER ROLE usr SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE stewardly TO usr;
\q
```
5. Configure the environment variables
```
cp .env.sample .env
```
Modify `.env` variable values to desired values.


6. Activate virtual env:
```
source venv/bin/activate
```
6. Install project dependencies:
```
pip install -r requirements.txt
```
    
    
Then simply apply the migrations:

    $ python manage.py migrate
    

You can now run the development server:

    $ python manage.py runserver