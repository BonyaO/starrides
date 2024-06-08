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

# NOTE: replace mydb and myuser with your preferred names
```

Modify [.env](./starrides/starrides/.env.example) file 
```shell
cp .env.example .env

# Replace the entries with the database details you created previously
```


#### Install required packages

```shell
# Move to the ./starrides/ directory and run the following command

pip3 install -r requirements.txt
```


#### Make and run the migrations
```shell
python3 manage.py makemigrations
python3 manage.py migrate
```
#### Manually add values into the Car Type Table
```shell
psql -U your_username -d your_database_name

INSERT INTO car_type (name) VALUES ('Sedan'), ('SUV'), ('Truck'), ('Coupe');

```
#### Create a superuser 
```shell
python3 manage.py createsuperuser
```

#### Runserver
```shell
python3 manage.py runserver
```
