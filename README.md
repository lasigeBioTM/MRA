# Multilingual Report Annotator

## Installation

### Use dev branch 

```
git checkout dev
```

### 1. Install Python requirements

```shell
pip install -r requirements.txt
```

### 2. Database

This code was developed assuming the use of MySQL. Could working with other RDBMS as well. 

If you don't haven't done it yet, install MySQL on your machine and create a database. I'm going to call this databaes 'mra'.

In config.cfg, you can now fill the value "SQLALCHEMY_DATABASE_URI":

```
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/mra'
```

### 3. Unbabel Account 

If you're working on this, you're probably in contact with someone from Unbabel or Faculty of Sciences. Ask around to see if you can get a username and API Key. Then, add it to `config.cfg`.

### 4. BioPortal API Key

You can get this after creating an account in their [website](http://bioportal.bioontology.org/). Then, add it to `config.cfg`.

### 5. ROOT_URL

If you're running this locally just write in `config.cfg`:

```
ROOT_URL = 'localhost'
```

### 6. Setup Celery Broker

Follow [this](http://docs.celeryproject.org/en/latest/getting-started/brokers/rabbitmq.html).

### 7. Create tables in Database 

Run:
```
python manage.py db upgrade
python manage.py db migrate 
```

## Run it!

First you have to start a celery worker:

```
celery -A mra.celery worker --loglevel=INFO
 ```
 
Then, in another terminal window, you can run the server:

```shell
python manage.py runserver
```
