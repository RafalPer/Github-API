Python 3.10.1
```
pip install -r requirements.txt
```
## Edit settings.py with your database
```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "",
        "USER": "",
        "PASSWORD": "",
        "HOST": "localhost",
    }
}
```

## Then run migrations
```
python manage.py migrate
```

# API endpoints
## Register
http://127.0.0.1:8000/auth/register/ POST

```
{
    "username": "",
    "password": "",
    "password2": "",
    "email": "",
    "first_name": "",
    "last_name": ""
}
```

## Login
http://127.0.0.1:8000/auth/login/ POST

```
{
    "username": "",
    "password": ""
}
```

## API add
Adds a project to our DB and API
http://127.0.0.1:8000/api/add POST
```
{
    "url": "https://github.com/RafalPer/Github-API"
}
```

## Detail Info
http://127.0.0.1:8000/api/detail_info/ GET

## Basic info
http://127.0.0.1:8000/api/basic_info/ GET

## Update project
http://127.0.0.1:8000/api/detail_info/{id}/ PUT

Send Json with project_id, commit_id and download_link with prevoius added project then update method will get newest data from Github API
```
{
    "id": 1,
    "download_link": "https://api.github.com/repos/RafalPer/Github-API/zipball/",
    "commit": {
        "id": 1
    }
}
```
