FROM python:3.12.3-slim-bullseye

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /usr/src/djangobnb_backend

# This is important to avoid buffering issues and
# see print statements in real-time in the terminal 
ENV PYTHONUNBUFFERED=1

# Upgrade pip
RUN pip install --upgrade pip

# Install netcat
RUN apt-get update && apt-get install -y netcat

# Copy the requirements file
COPY ./requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the entrypoint script
COPY ./entrypoint.sh .

# Change the entrypoint script to use Unix line endings
RUN sed -i 's/\r$//g' /usr/src/djangobnb_backend/entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /usr/src/djangobnb_backend/entrypoint.sh

# Copy the rest of the application code
COPY . .

# Change the entrypoint script to use Unix line endings
ENTRYPOINT [ "/usr/src/djangobnb_backend/entrypoint.sh" ]

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
