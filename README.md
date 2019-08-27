## Installation
1) pip install -r requirements/dev.txt 
2) Create env.json file in root folder
    ##### env.json config file example:
    ```json
    {
        "SECRET_KEY": "secrete key",
        "DB_NAME": "tracker",
        "DB_USER": "user",
        "DB_PASSWORD": "password",
        "DB_HOST": "127.0.0.1",
        "DB_PORT": 3306,
        "DEBUG": true,
        "EMAIL_HOST": "smtp.mailtrap.io",
        "EMAIL_PORT": 2525,
        "EMAIL_HOST_USER": "user",
        "EMAIL_HOST_PASSWORD": "password",
        "EMAIL_USE_SSL": true,
        "EMAIL_USE_TLS": false
    }
    ```
3) Create database
4) python manage.py makemigrations
5) python manage.py migrate
6) python manage.py createsuperuser
7) Run test server: python manage.py runserver 127.0.0.1:8080
