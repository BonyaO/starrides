# starrides
StarRides: Car Rental App is a school project to build a platform for people to rent cars. 


## Project Setup

#### Create Python environment
```shell
python3 -m venv venv
source venv/bin/active

```

#### Create your database and set environment variables
Create Database
```shell
sudo -u postgres psql

CREATE DATABASE mydb

CREATE USER myuser WITH ENCRYPTED PASSWORD 'mypass';

GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
```

Modify [.env](./starrides/starrides/.env.example) file 
```shell
cp .env.example .env

# Enter your database details you created previously
```

#### Install requirement packages

```shell
# Move to the ./starrides/ directory and run the following command

pip3 install -r requirements.txt
```

