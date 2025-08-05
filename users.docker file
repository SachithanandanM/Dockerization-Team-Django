# Base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory inside container
WORKDIR /app

# Install system dependencies (if needed for psycopg2, mysqlclient, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the users app and necessary Django files
COPY manage.py /app/
COPY ecommerce /app/ecommerce
COPY users /app/users

# Expose port 8000
EXPOSE 8000

# Run only the Django server for this project
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
