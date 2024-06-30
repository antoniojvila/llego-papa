# Django Project with Docker

This project sets up a Django application with Docker, including PostgreSQL as the database.

## Setup Instructions

### 1. Build and Start the Containers

Build the Docker images:

```sh
docker-compose build
```

### 2. Create superuser

create superuser defaulr:

```sh
docker-compose up -d
docker-compose exec web python manage.py createsuperuser
username: admin
email: admin@gmail.com
password: admin
verify_password: admin

```
Nota: solo ingresar los valores para crear la cuenta del superuser segun lo vaya pidiendo la consola

### 3. load units and lessons

```
docker-compose exec web python load_units_lessons.py
```
### 4. Access the Application

Once the containers are running, you can access the Django application in your web browser at the following URL:

```
http://127.0.0.1:8000/games/1/ or
http://127.0.0.1:8000/games/2/
```

Feel free to adjust the URL as needed for your specific setup.