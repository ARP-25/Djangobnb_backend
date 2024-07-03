# Djangobnb

![Djangobnb](https://res.cloudinary.com/dbui0ebjv/image/upload/v1720020057/djangobnb_screenshot_cbh0fw.png)

## About the Project

Djangobnb is a Airbnb-like application developed with a modern tech stack. The application includes both frontend and backend components, is containerized, and is deployed in a production-like environment. We use Nginx to serve the application securely over HTTPS. SSL certificates are created and auto-renewed every 12 hours to ensure secure communication.

## Tech Stack

-   **Frontend:** Next.js, React, Tailwind CSS, TypeScript
-   **Backend:** Django, Python, PostgreSQL
-   **DevOps:** Docker, Nginx, DigitalOcean, Certbot
-   **Version Control:** Git, GitHub

## Features

-   User registration and login (simplejwt)
-   Accommodation search and booking
-   Real-time Chat (websocket)
-   Wishlist

## Installation

### Prerequisites

-   Docker
-   Docker Compose
-   Python 3.x
-   Node.js
-   npm or yarn

### Backend

1. Clone the repository:
    ```bash
    git clone https://github.com/ARP-25/Djangobnb_backend.git
    ```
2. Create a virtual environment and install dependencies:
    ```bash
    cd Djangobnb_backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
3. Apply the migrations:
    ```bash
    python manage.py migrate
    ```
4. Start the development server:
    ```bash
    python manage.py runserver
    ```

### Frontend

1. Clone the repository:
    ```bash
    git clone https://github.com/ARP-25/Djangobnb_frontend.git
    ```
2. Install dependencies:
    ```bash
    cd Djangobnb_frontend
    npm install
    # or
    yarn install
    ```
3. Start the development server:
    ```bash
    npm run dev
    # or
    yarn dev
    ```

## Docker

1. Clone the both front- and backend repository:
    ```bash
    git clone https://github.com/ARP-25/Djangobnb_frontend.git
    git clone https://github.com/ARP-25/Djangobnb_backend.git
    cd Djangobnb_backend
    ```
2. Start the application with Docker Compose:
    ```bash
    docker-compose.ssl.yml up --build
    ```

## Deployment

### Infrastructure

The application is deployed on DigitalOcean using the following infrastructure components:

-   **DigitalOcean Droplets:** Virtual machines that host the application.
-   **Nginx:** Acts as a reverse proxy to manage and direct traffic to the Docker containers.
-   **Docker Compose:** Orchestrates the multi-container Docker applications, ensuring that all services (frontend, backend, database) are up and running.
-   **Certbot:** Automates the process of obtaining and renewing SSL certificates.

### Diagram

![Infrastructure Diagram](https://res.cloudinary.com/dbui0ebjv/image/upload/v1720021834/Infrastructure_gyy8gw.png)

### Deployment Steps

1. **Create a DigitalOcean Droplet:**

    - Set up a new droplet with your preferred OS (e.g., Ubuntu).
    - Configure the droplet with necessary firewall rules and SSH access.

2. **Install Docker and Docker Compose:**

    - SSH into the droplet and install Docker:
        ```bash
        sudo apt-get update
        sudo apt-get install -y docker.io
        ```
    - Install Docker Compose:
        ```bash
        sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
        ```

3. **Clone the Repository:**

    - Clone project front- and backend repository onto the droplet:
        ```bash
        git clone https://github.com/ARP-25/Djangobnb_backend
        git clone https://github.com/ARP-25/frontend.git
        cd Djangobnb_backend
        ```

4. **Configure Nginx and Certbot:**

    - Set up Nginx to serve the frontend and proxy requests to the backend.
    - Use Certbot to obtain and renew SSL certificates.

5. **Deploy with Docker Compose:**
    - Start the application using Docker Compose:
        ```bash
        docker-compose -f docker-compose.sll.yml up --build
        ```

## Docker Compose Configuration

```yaml
version: "3.8"

services:
    nginx:
        build: ./nginx
        ports:
            - "80:80"
            - "443:443"
        depends_on:
            - web
            - daphne
            - frontend
        volumes:
            - media_volume:/usr/src/djangobnb_backend/media
            - static_volume:/usr/src/djangobnb_backend/static
            - /var/www/certbot:/var/www/certbot
            - /var/certbot/conf:/etc/letsencrypt
            - /webapps/Djangobnb_backend/nginx/nginx.conf:/etc/nginx/nginx.conf
        networks:
            - app-network
        restart: unless-stopped

    web:
        build: ./djangobnb_backend
        command: gunicorn djangobnb_backend.wsgi:application --bind 0.0.0.0:8000
        volumes:
            - ./djangobnb_backend/:/usr/src/djangobnb_backend/
            - media_volume:/usr/src/djangobnb_backend/media
            - static_volume:/usr/src/djangobnb_backend/static
        expose:
            - "8000"
        env_file:
            - ./.env
        depends_on:
            - db
        networks:
            - app-network

    daphne:
        build: ./djangobnb_backend
        command: daphne --bind 0.0.0.0 -p 8002 djangobnb_backend.asgi:application
        expose:
            - "8002"
        env_file:
            - ./.env
        depends_on:
            - db
        networks:
            - app-network

    frontend:
        build: ../Djangobnb_frontend
        expose:
            - "3000"
        networks:
            - app-network

    db:
        image: postgres:15
        volumes:
            - postgres_data:/var/lib/postgresql/data/
        environment:
            - POSTGRES_USER=postgresuser
            - POSTGRES_PASSWORD=postgrespassword
            - POSTGRES_DB=djangobnb
        networks:
            - app-network

    certbot:
        image: certbot/certbot:latest
        volumes:
            - /var/certbot/conf:/etc/letsencrypt
            - /var/www/certbot:/var/www/certbot
        depends_on:
            - nginx
        networks:
            - app-network

networks:
    app-network:
        driver: bridge

volumes:
    postgres_data:
    media_volume:
    static_volume:
```

## Nginx Configuration

```conf
upstream djangobnb_backend {
    server web:8000;
}

upstream djangobnb_daphne {
    server daphne:8002;
}

upstream djangobnb_frontend {
    server frontend:3000;
}

server {
    listen 80;
    server_name djangobnb.com www.djangobnb.com;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
        allow all;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name djangobnb.com www.djangobnb.com;

    ssl_certificate /etc/letsencrypt/live/djangobnb.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/djangobnb.com/privkey.pem;

    # Frontend
    location / {
        proxy_pass http://djangobnb_frontend;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }

    # Backend
    location /admin/ {
        proxy_pass http://djangobnb_backend/admin/;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }

    location /api/properties/ {
        proxy_pass http://djangobnb_backend/api/properties/;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }

    location /api/auth/ {
        proxy_pass http://djangobnb_backend/api/auth/;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }

    location /api/chat/ {
        proxy_pass http://djangobnb_backend/api/chat/;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }

    location /media/ {
        alias /usr/src/djangobnb_backend/media/;
    }

    location /static/ {
        alias /usr/src/djangobnb_backend/static/;
    }

    location ~^/ws/ {
        proxy_pass http://djangobnb_daphne;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
        allow all;
    }

    error_page 404 /404.html;
    location = /404.html {
        internal;
    }

    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        internal;
    }
}

```

## Contributing

Contributions are welcome! Please open an issue before submitting a pull request.

## Contact

Angelo Rocco Pucci - [in/angeloroccopucci/](https://www.linkedin.com/in/angeloroccopucci/) - angelo.pucci@outlook.de - [angeloroccopucci.com](angeloroccopucci.com)

Project Link Frontend: [https://github.com/ARP-25/Djangobnb_frontend](https://github.com/ARP-25/Djangobnb_frontend)

Project Link Backend: [https://github.com/ARP-25/Djangobnb_backend](https://github.com/ARP-25/Djangobnb_backend)
