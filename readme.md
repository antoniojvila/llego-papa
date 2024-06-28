# Django Project with Docker

This project sets up a Django application with Docker, including PostgreSQL as the database.

## Setup Instructions

### 1. Build and Start the Containers

Build the Docker images and start the containers:

```sh
docker-compose up --build
```

### 2. Run Migrations

Apply the database migrations to create the necessary tables:

```sh
docker-compose run web python manage.py migrate
docker-compose run web python manage.py create_superuser --noinput

```

### 3. Access the Application

Once the containers are running, you can access the Django application in your web browser at the following URL (replace `your-domain.com` with your actual domain or IP address):

```
http://your-domain.com:8000
```

Feel free to adjust the URL as needed for your specific setup.